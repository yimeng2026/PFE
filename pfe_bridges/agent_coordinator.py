#!/usr/bin/env python3
"""
pfe-bridges/agent_coordinator.py — PFE 多代理协调器

基于千界花园 research-prompts.ts 的 9 种学术协作类型，
适配为 PFE 工程协作类型，调度多个桥接模块并行验证不同千年难题。

PFE ENGINEERING NOTE: 协调器是涌现控制层，不保证全局最优，
追求局部有效性和快速反馈循环。
"""

import asyncio
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable, Type
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum
import json
from pathlib import Path

from .base_bridge import PFEProblemBridge, BridgeRunResult, BridgeStatus, HeuristicStrategy
from .qianjie_bridge import QianJieClient, QianJieConfig, LLMStrategyRequest


# ─── 工程协作类型（映射自千界花园 9 种学术类型）───

class PFEEngineeringMode(Enum):
    """
    PFE 工程协作模式 — 从千界花园学术类型映射而来。
    
    学术类型 → 工程类型映射：
    - expert_panel     → ENGINEERING_PANEL   : 工程专家组审议
    - workshop         → SWARM_BRAINSTORM    : 涌现头脑风暴
    - pipeline         → PIPELINE_STAGE      : 分阶段验证管道
    - review_board     → CODE_REVIEW         : 代码/数值审查
    - competition      → STRATEGY_COMPETE    : 策略竞赛
    - mentorship       → KNOWLEDGE_TRANSFER  : 知识迁移（PFE → SYLVA）
    - code_review      → VERIFICATION_AUDIT  : 验证审计
    - validation       → CROSS_VERIFY        : 交叉验证
    - task_force       → TASK_DISPATCH       : 任务分发
    """
    ENGINEERING_PANEL = "engineering_panel"
    SWARM_BRAINSTORM = "swarm_brainstorm"
    PIPELINE_STAGE = "pipeline_stage"
    CODE_REVIEW = "code_review"
    STRATEGY_COMPETE = "strategy_compete"
    KNOWLEDGE_TRANSFER = "knowledge_transfer"
    VERIFICATION_AUDIT = "verification_audit"
    CROSS_VERIFY = "cross_verify"
    TASK_DISPATCH = "task_dispatch"


# 学术 → 工程映射表
ACADEMIC_TO_ENGINEERING: Dict[str, PFEEngineeringMode] = {
    "expert_panel": PFEEngineeringMode.ENGINEERING_PANEL,
    "workshop": PFEEngineeringMode.SWARM_BRAINSTORM,
    "pipeline": PFEEngineeringMode.PIPELINE_STAGE,
    "review_board": PFEEngineeringMode.CODE_REVIEW,
    "competition": PFEEngineeringMode.STRATEGY_COMPETE,
    "mentorship": PFEEngineeringMode.KNOWLEDGE_TRANSFER,
    "code_review": PFEEngineeringMode.VERIFICATION_AUDIT,
    "validation": PFEEngineeringMode.CROSS_VERIFY,
    "task_force": PFEEngineeringMode.TASK_DISPATCH,
}

ENGINEERING_TO_ACADEMIC: Dict[PFEEngineeringMode, str] = {
    v: k for k, v in ACADEMIC_TO_ENGINEERING.items()
}


# ─── 千界花园原生协作类型与学科枚举（匹配 collaborations/init 端点）───

class QianJieCollaborationType(Enum):
    """
    千界花园 5 种协作类型（匹配 /api/research/collaborations/init 端点）。

    PFE 协调器可直接使用这些类型调用千界花园 API，
    无需经过 ACADEMIC_TO_ENGINEERING 映射。
    """
    FULL_RESEARCH = "full_research"
    THEOREM_PROVING = "theorem_proving"
    PAPER_WRITING = "paper_writing"
    PEER_REVIEW = "peer_review"
    EDUCATIONAL = "educational"


class QianJieDomain(Enum):
    """
    千界花园 3 个学科模板（匹配 collaborations/init 端点 EXPERT_TEMPLATES）。

    每个学科对应一组预置专家角色（lead_validator / validator / checker）。
    """
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    AI = "ai"
    INTERDISCIPLINARY = "interdisciplinary"


@dataclass
class AgentTask:
    """单个代理任务。"""
    task_id: str
    problem_name: str
    bridge_class: Type[PFEProblemBridge]
    bridge_instance: Optional[PFEProblemBridge] = None
    mode: PFEEngineeringMode = PFEEngineeringMode.TASK_DISPATCH
    context: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5  # 1-10, 越高越优先
    status: BridgeStatus = BridgeStatus.IDLE
    result: Optional[BridgeRunResult] = None
    error: Optional[str] = None
    start_time: float = 0.0
    end_time: float = 0.0


@dataclass
class CoordinatorConfig:
    """协调器配置。"""
    max_workers: int = 4
    timeout_per_task: float = 300.0
    retry_failed: bool = True
    max_retries: int = 1
    qianjie_config: Optional[QianJieConfig] = None
    cache_dir: Optional[str] = None
    auto_push_results: bool = True  # 自动回传千界花园


@dataclass
class CoordinatorReport:
    """协调器运行报告。"""
    session_id: str
    start_time: float
    end_time: float
    tasks: List[AgentTask] = field(default_factory=list)
    overall_status: BridgeStatus = BridgeStatus.IDLE
    average_confidence: float = 0.0
    verified_count: int = 0
    failed_count: int = 0
    partial_count: int = 0
    strategies_generated: int = 0
    qianjie_pushed: int = 0
    markdown_summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "duration_ms": int((self.end_time - self.start_time) * 1000),
            "overall_status": self.overall_status.value,
            "average_confidence": round(self.average_confidence, 3),
            "verified_count": self.verified_count,
            "failed_count": self.failed_count,
            "partial_count": self.partial_count,
            "strategies_generated": self.strategies_generated,
            "qianjie_pushed": self.qianjie_pushed,
            "tasks": [
                {
                    "task_id": t.task_id,
                    "problem": t.problem_name,
                    "status": t.status.value,
                    "confidence": t.result.confidence_summary if t.result else 0.0,
                    "duration_ms": int((t.end_time - t.start_time) * 1000) if t.end_time > 0 else 0,
                    "error": t.error,
                }
                for t in self.tasks
            ],
        }


class PFEAgentCoordinator:
    """
    PFE 多代理协调器。

    负责：
    1. 注册多个桥接模块（每个对应一个千年难题）
    2. 根据工程协作模式调度任务
    3. 并行执行数值验证
    4. 聚合结果、生成综合报告
    5. 回传千界花园
    """

    def __init__(self, config: Optional[CoordinatorConfig] = None):
        self.config = config or CoordinatorConfig()
        self.qianjie = QianJieClient(self.config.qianjie_config)
        self._bridges: Dict[str, Type[PFEProblemBridge]] = {}
        self._bridge_instances: Dict[str, PFEProblemBridge] = {}
        self._task_history: List[CoordinatorReport] = []
        self._session_counter = 0

    def register_bridge(self, problem_name: str, bridge_class: Type[PFEProblemBridge]) -> None:
        """注册一个桥接模块。"""
        self._bridges[problem_name] = bridge_class
        print(f"[Coordinator] Registered bridge: {problem_name} -> {bridge_class.__name__}")

    def create_task(
        self,
        problem_name: str,
        mode: PFEEngineeringMode = PFEEngineeringMode.TASK_DISPATCH,
        context: Optional[Dict[str, Any]] = None,
        priority: int = 5,
    ) -> AgentTask:
        """创建单个任务。"""
        if problem_name not in self._bridges:
            raise ValueError(f"No bridge registered for problem: {problem_name}")

        self._session_counter += 1
        return AgentTask(
            task_id=f"pfe-{self._session_counter:04d}-{problem_name}",
            problem_name=problem_name,
            bridge_class=self._bridges[problem_name],
            mode=mode,
            context=context or {},
            priority=priority,
        )

    def _execute_single_task(self, task: AgentTask) -> AgentTask:
        """执行单个任务（线程安全）。"""
        task.start_time = time.time()
        task.status = BridgeStatus.RUNNING

        try:
            # 获取或创建桥接实例
            if task.problem_name not in self._bridge_instances:
                bridge_class = task.bridge_class
                # 如果桥接类支持 QianJieClient，注入它
                init_kwargs = {}
                if hasattr(bridge_class, "client"):
                    init_kwargs["client"] = self.qianjie
                if hasattr(bridge_class, "cache_dir"):
                    init_kwargs["cache_dir"] = self.config.cache_dir
                self._bridge_instances[task.problem_name] = bridge_class(task.problem_name, **init_kwargs)

            bridge = self._bridge_instances[task.problem_name]
            result = bridge.run_pipeline(task.context)
            task.result = result
            task.status = result.status
            task.end_time = time.time()

        except Exception as e:
            task.status = BridgeStatus.FAILED
            task.error = str(e)
            task.end_time = time.time()

        return task

    def run_parallel(self, tasks: List[AgentTask]) -> CoordinatorReport:
        """
        并行执行多个任务。

        使用 ThreadPoolExecutor 并行运行不同桥接模块的验证管道。
        每个桥接模块内部可能有更细粒度的并行（如 numpy/scipy）。
        """
        session_id = f"pfe-session-{int(time.time())}"
        start_time = time.time()

        print(f"[Coordinator] Session {session_id}: {len(tasks)} tasks, max_workers={self.config.max_workers}")

        completed_tasks: List[AgentTask] = []
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            future_to_task = {
                executor.submit(self._execute_single_task, task): task
                for task in tasks
            }

            for future in as_completed(future_to_task, timeout=self.config.timeout_per_task * len(tasks)):
                task = future_to_task[future]
                try:
                    completed = future.result()
                    completed_tasks.append(completed)
                    print(f"[Coordinator] Task {completed.task_id}: {completed.status.value} (confidence={completed.result.confidence_summary if completed.result else 0:.2f})")
                except Exception as e:
                    task.status = BridgeStatus.FAILED
                    task.error = str(e)
                    task.end_time = time.time()
                    completed_tasks.append(task)
                    print(f"[Coordinator] Task {task.task_id}: FAILED - {e}")

        # 聚合结果
        report = self._aggregate_report(session_id, start_time, completed_tasks)

        # 自动回传千界花园
        if self.config.auto_push_results:
            self._push_to_qianjie(report)

        self._task_history.append(report)
        return report

    def run_sequential(self, tasks: List[AgentTask]) -> CoordinatorReport:
        """串行执行（用于依赖链）。"""
        session_id = f"pfe-seq-{int(time.time())}"
        start_time = time.time()

        completed_tasks: List[AgentTask] = []
        for task in tasks:
            completed = self._execute_single_task(task)
            completed_tasks.append(completed)
            # 将前一个任务的结果注入下一个任务的上下文
            if completed.result and len(tasks) > len(completed_tasks):
                next_task = tasks[len(completed_tasks)]
                next_task.context["previous_result"] = completed.result.to_dict() if hasattr(completed.result, "to_dict") else str(completed.result)

        report = self._aggregate_report(session_id, start_time, completed_tasks)
        if self.config.auto_push_results:
            self._push_to_qianjie(report)
        self._task_history.append(report)
        return report

    def _aggregate_report(self, session_id: str, start_time: float, tasks: List[AgentTask]) -> CoordinatorReport:
        """聚合所有任务结果为报告。"""
        end_time = time.time()

        verified = sum(1 for t in tasks if t.status == BridgeStatus.SUCCESS)
        failed = sum(1 for t in tasks if t.status == BridgeStatus.FAILED)
        partial = sum(1 for t in tasks if t.status == BridgeStatus.PARTIAL)

        confidences = [t.result.confidence_summary for t in tasks if t.result]
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

        strategies = sum(
            len(t.result.strategies) for t in tasks if t.result
        )

        overall = BridgeStatus.SUCCESS if verified == len(tasks) and len(tasks) > 0 else \
                  BridgeStatus.PARTIAL if partial > 0 or verified > 0 else BridgeStatus.FAILED

        report = CoordinatorReport(
            session_id=session_id,
            start_time=start_time,
            end_time=end_time,
            tasks=tasks,
            overall_status=overall,
            average_confidence=avg_conf,
            verified_count=verified,
            failed_count=failed,
            partial_count=partial,
            strategies_generated=strategies,
        )

        report.markdown_summary = self._generate_markdown_summary(report)
        return report

    def _generate_markdown_summary(self, report: CoordinatorReport) -> str:
        """生成 Markdown 总结报告。"""
        lines = [
            f"# PFE Agent Coordinator Report",
            f"",
            f"**Session**: {report.session_id}",
            f"**Duration**: {int((report.end_time - report.start_time) * 1000)}ms",
            f"**Overall Status**: {report.overall_status.value}",
            f"**Average Confidence**: {report.average_confidence:.2f}",
            f"",
            f"## Summary",
            f"- ✅ Verified: {report.verified_count}",
            f"- ⚠️ Partial: {report.partial_count}",
            f"- ❌ Failed: {report.failed_count}",
            f"- 🧠 Strategies Generated: {report.strategies_generated}",
            f"- 📤 Pushed to QianJie: {report.qianjie_pushed}",
            f"",
            f"## Task Details",
            f"",
        ]
        for t in report.tasks:
            emoji = "✅" if t.status == BridgeStatus.SUCCESS else "⚠️" if t.status == BridgeStatus.PARTIAL else "❌"
            lines.append(f"### {emoji} {t.problem_name} ({t.task_id})")
            lines.append(f"- Status: {t.status.value}")
            if t.result:
                lines.append(f"- Confidence: {t.result.confidence_summary:.2f}")
                lines.append(f"- Numerical Results: {len(t.result.numerical_results)}")
                lines.append(f"- Strategies: {len(t.result.strategies)}")
            if t.error:
                lines.append(f"- Error: `{t.error}`")
            lines.append("")
        return "\n".join(lines)

    def _push_to_qianjie(self, report: CoordinatorReport) -> None:
        """将协调器报告回传到千界花园。"""
        try:
            resp = self.qianjie.push_verification_result(
                BridgeRunResult(
                    problem_name="PFE-AgentCoordinator",
                    status=report.overall_status,
                    confidence_summary=report.average_confidence,
                    report_markdown=report.markdown_summary,
                    metadata={"verified": report.verified_count, "failed": report.failed_count, "partial": report.partial_count},
                )
            )
            if resp.get("success"):
                report.qianjie_pushed += 1
                print(f"[Coordinator] Pushed report to QianJie: {resp.get('data', {}).get('id', 'ok')}")
            else:
                print(f"[Coordinator] Push failed: {resp.get('error')}")
        except Exception as e:
            print(f"[Coordinator] Push error: {e}")

    def get_qianjie_status(self) -> Dict[str, Any]:
        """获取千界花园连接状态。"""
        return self.qianjie.health_check()

    # ─── 千界花园核心集成方法（新增） ───

    def initialize_millennium_problem(self, problem_id: Optional[str] = None) -> Dict[str, Any]:
        """
        调用 MillenniumInitClient 初始化千年难题研究生态。

        对应千界花园 /api/research/millennium/init 端点。
        如果千界花园未运行，返回包含 fallback 标志的响应。

        Args:
            problem_id: 可选，指定问题 ID（如 "p-vs-np"），
                       但千界花园端点会一次性初始化所有 4 个千年难题。

        Returns:
            千界花园 API 响应，包含 {success, data: {problems: [...]}}
        """
        try:
            result = self.qianjie.millennium.init()
            if result.get("success"):
                problems = result.get("data", {}).get("problems", [])
                print(
                    f"[Coordinator] Initialized {len(problems)} millennium problems"
                    + (f" [{problem_id}]" if problem_id else "")
                )
            else:
                print(f"[Coordinator] Millennium init failed: {result.get('error')}")
            return result
        except Exception as e:
            print(f"[Coordinator] Millennium init exception: {e}")
            return {"success": False, "error": str(e), "fallback": True}

    def sync_sylva_to_qianjie(
        self,
        toe_sylva_path: Optional[str] = None,
        analyze_with_llm: bool = True,
        create_tasks: bool = True,
    ) -> Dict[str, Any]:
        """
        调用 SylvaParserClient 解析 TOE-SYLVA 文件并同步到千界花园。

        策略：
        1. 优先调用千界花园 /api/research/sylva-sync 端点（千界花园在线时）
        2. 如果 API 不可用，使用本地 SylvaParserClient 解析 Lean 文件
        3. 将解析结果通过 ResearchNoteClient 推送到千界花园 notes

        Args:
            toe_sylva_path: TOE-SYLVA 本地路径，默认使用记忆中的路径
            analyze_with_llm: 是否启用 LLM 分析 sorry（仅 API 模式有效）
            create_tasks: 是否为 sorry 创建 AcademicTask（仅 API 模式有效）

        Returns:
            同步结果 dict，包含 mode（api_sync 或 local_parse）、统计信息
        """
        # 阶段 1: 尝试通过千界花园 API 同步
        try:
            result = self.qianjie.sync_sylva(
                analyze_with_llm=analyze_with_llm, create_tasks=create_tasks
            )
            status = self.qianjie.get_sylva_status()
            if status.files_parsed > 0 or result.raw_response.get("success"):
                print(
                    f"[Coordinator] SYLVA API sync: {status.files_parsed} files, "
                    f"{status.sorry_total} sorry, {status.modules_total} modules"
                )
                return {
                    "success": True,
                    "mode": "api_sync",
                    "files_parsed": status.files_parsed,
                    "modules_total": status.modules_total,
                    "theorems_total": status.theorems_total,
                    "sorry_total": status.sorry_total,
                    "raw_response": result.raw_response,
                }
        except Exception as e:
            print(f"[Coordinator] API sync failed, falling back to local parser: {e}")

        # 阶段 2: Fallback — 本地解析 + 推送 notes
        try:
            from pathlib import Path
            toe_path = Path(
                toe_sylva_path
                or "C:\\Users\\一梦\\Documents\\TOE-SYLVA-pull"
            )
            files: List[Dict[str, str]] = []
            for lean_file in toe_path.rglob("*.lean"):
                path_str = str(lean_file)
                if ".lake" in path_str or "lake-packages" in path_str:
                    continue
                content = lean_file.read_text(encoding="utf-8")
                files.append({
                    "path": str(lean_file.relative_to(toe_path)).replace("\\", "/"),
                    "content": content,
                })

            parser = self.qianjie.parser
            parsed = parser.parse_sylva_project(files)

            # 将解析结果推送到千界花园 notes
            notes_created = 0
            for module in parsed.modules:
                note_result = self.qianjie.notes.create_note(
                    title=f"SYLVA解析: {module.fileName}",
                    content=json.dumps(
                        {
                            "filePath": module.filePath,
                            "totalLines": module.totalLines,
                            "theoremCount": len(module.theorems),
                            "definitionCount": len(module.definitions),
                            "sorryCount": module.sorryCount,
                            "theorems": [asdict(t) for t in module.theorems],
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    tags=["sylva-sync", "local-parse", module.fileName],
                )
                if note_result.get("success"):
                    notes_created += 1

            print(
                f"[Coordinator] Local parse: {len(files)} files, "
                f"{parsed.totalSorry} sorry, {notes_created} notes pushed"
            )
            return {
                "success": True,
                "mode": "local_parse",
                "files_parsed": len(files),
                "modules_total": len(parsed.modules),
                "theorems_total": parsed.totalTheorems,
                "sorry_total": parsed.totalSorry,
                "notes_created": notes_created,
            }
        except Exception as e:
            print(f"[Coordinator] Local parse fallback failed: {e}")
            return {"success": False, "error": str(e), "fallback": True}

    def init_qianjie_collaboration(
        self,
        domain: QianJieDomain,
        topic: str,
        collaboration_type: QianJieCollaborationType,
    ) -> Dict[str, Any]:
        """
        使用千界花园 5 种协作类型和 3 个学科模板初始化协作生态。

        对应 /api/research/collaborations/init 端点。

        Args:
            domain: 学科领域（mathematics / physics / ai / interdisciplinary）
            topic: 研究主题
            collaboration_type: 协作类型（full_research / theorem_proving / ...）
        """
        try:
            result = self.qianjie.collaborations.init_collaboration(
                domain=domain.value,
                topic=topic,
                collaboration_type=collaboration_type.value,
            )
            if result.get("success"):
                print(
                    f"[Coordinator] Collaboration init OK: {collaboration_type.value} "
                    f"in {domain.value} for '{topic}'"
                )
            else:
                print(f"[Coordinator] Collaboration init failed: {result.get('error')}")
            return result
        except Exception as e:
            print(f"[Coordinator] Collaboration init exception: {e}")
            return {"success": False, "error": str(e), "fallback": True}

    def create_qianjie_panel(
        self,
        name: str,
        description: str = "",
        domain: QianJieDomain = QianJieDomain.INTERDISCIPLINARY,
        strategy: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        通过 AcademicPanelClient 创建千界花园专家组。

        对应 /api/research/panels 端点。
        """
        try:
            result = self.qianjie.panels.create_panel(
                name=name,
                description=description,
                domain=domain.value,
                strategy=strategy or {},
            )
            if result.get("success"):
                print(f"[Coordinator] Panel created: {name}")
            else:
                print(f"[Coordinator] Panel create failed: {result.get('error')}")
            return result
        except Exception as e:
            print(f"[Coordinator] Panel create exception: {e}")
            return {"success": False, "error": str(e), "fallback": True}

    def dispatch_by_mode(
        self,
        problem_names: List[str],
        mode: PFEEngineeringMode = PFEEngineeringMode.TASK_DISPATCH,
        shared_context: Optional[Dict[str, Any]] = None,
    ) -> CoordinatorReport:
        """
        按工程模式批量分发任务。

        例如：
        - CROSS_VERIFY: 所有桥接模块对同一个数值目标进行交叉验证
        - STRATEGY_COMPETE: 多个 LLM 策略竞争，选最优
        - PIPELINE_STAGE: 按顺序执行，前一阶段结果传入下一阶段
        """
        tasks = []
        for i, name in enumerate(problem_names):
            ctx = dict(shared_context or {})
            ctx["mode"] = mode.value
            ctx["batch_index"] = i
            ctx["batch_total"] = len(problem_names)
            tasks.append(self.create_task(name, mode=mode, context=ctx, priority=5))

        if mode in (PFEEngineeringMode.PIPELINE_STAGE, PFEEngineeringMode.KNOWLEDGE_TRANSFER):
            return self.run_sequential(tasks)
        else:
            return self.run_parallel(tasks)

    def get_history(self) -> List[CoordinatorReport]:
        """获取历史运行记录。"""
        return self._task_history

    def save_history(self, path: Optional[str] = None) -> str:
        """保存历史记录到文件。"""
        save_path = Path(path or self.config.cache_dir or ".") / "coordinator_history.json"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(
                [r.to_dict() for r in self._task_history],
                f,
                ensure_ascii=False,
                indent=2,
            )
        return str(save_path)
