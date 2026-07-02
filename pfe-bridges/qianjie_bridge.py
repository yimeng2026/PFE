#!/usr/bin/env python3
"""
pfe-bridges/qianjie_bridge.py — 千界花园后端桥接模块

连接 PFE 工程原型与千界花园 (Blooming Garden) 学术研究系统。
通过 HTTP API 调用千界花园的 research 服务，实现：
- 获取 TOE-SYLVA 状态同步
- 调用千界花园 LLM 进行工程策略生成
- 解析千界花园 JSON 数据
- 回传 PFE 验证结果

PFE ENGINEERING NOTE: 这是工程集成层，不追求形式化严格，
追求 PFE 与千界花园之间的有效数据涌现。
"""

import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import urllib.request
import urllib.error

from .base_bridge import PFEProblemBridge, BridgeStatus, NumericalVerificationResult, HeuristicStrategy, BridgeRunResult


@dataclass
class QianJieConfig:
    """千界花园连接配置。"""
    base_url: str = "http://localhost:3000"  # 千界花园默认开发端口
    api_prefix: str = "/api/research"
    timeout: int = 30
    max_retries: int = 2
    retry_delay: float = 1.0


@dataclass
class SylvaSyncStatus:
    """TOE-SYLVA 同步状态。"""
    files_parsed: int = 0
    modules_total: int = 0
    theorems_total: int = 0
    definitions_total: int = 0
    sorry_total: int = 0
    axiom_total: int = 0
    millennium_problems: List[str] = field(default_factory=list)
    top_modules: List[Dict[str, Any]] = field(default_factory=list)
    active_research: List[Dict[str, Any]] = field(default_factory=list)
    recent_tasks: List[Dict[str, Any]] = field(default_factory=list)
    sync_history: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class LLMStrategyRequest:
    """请求千界花园 LLM 生成策略的上下文。"""
    collaboration_type: str  # 9种之一: expert_panel, workshop, pipeline, review_board, competition, mentorship, code_review, validation, task_force
    topic: str
    domain: str = "mathematics"
    mode: str = "engineering"
    role: str = "PFE Engineer"
    specialty: str = "numerical verification"
    previous_content: str = ""
    target_module: str = ""
    target_paper: str = ""
    temperature: float = 0.4
    max_tokens: int = 4096


class QianJieClient:
    """
    千界花园 HTTP API 客户端。

    封装对千界花园 /api/research/* 端点的调用，提供：
    - GET/POST 通用请求
    - 错误重试
    - JSON 解析
    - 响应缓存
    """

    def __init__(self, config: Optional[QianJieConfig] = None):
        self.config = config or QianJieConfig()
        self._cache: Dict[str, Any] = {}
        self._last_request_time: float = 0.0
        self._min_interval: float = 0.5  # 请求间隔，避免过快

    def _make_request(
        self,
        method: str,
        endpoint: str,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """发送 HTTP 请求并返回 JSON 响应。"""
        url = f"{self.config.base_url}{self.config.api_prefix}{endpoint}"
        request_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if headers:
            request_headers.update(headers)

        data = json.dumps(body).encode("utf-8") if body else None
        req = urllib.request.Request(
            url,
            data=data,
            headers=request_headers,
            method=method,
        )

        # 速率限制
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)

        last_error = None
        for attempt in range(self.config.max_retries + 1):
            try:
                self._last_request_time = time.time()
                with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                last_error = e
                if e.code in (429, 500, 502, 503) and attempt < self.config.max_retries:
                    time.sleep(self.config.retry_delay * (2 ** attempt))
                    continue
                # 尝试读取错误响应体
                try:
                    body_text = e.read().decode("utf-8")
                    return json.loads(body_text)
                except Exception:
                    return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
            except Exception as e:
                last_error = e
                if attempt < self.config.max_retries:
                    time.sleep(self.config.retry_delay * (2 ** attempt))
                    continue
                return {"success": False, "error": str(e)}

        return {"success": False, "error": str(last_error) if last_error else "Unknown error"}

    # ─── 千界花园 API 封装 ───

    def sync_sylva(self, analyze_with_llm: bool = True, create_tasks: bool = True) -> SylvaSyncStatus:
        """
        POST /api/research/sylva-sync
        触发 TOE-SYLVA 同步，获取最新 Lean 解析状态。
        """
        resp = self._make_request(
            "POST",
            "/sylva-sync",
            body={"analyzeWithLLM": analyze_with_llm, "createTasks": create_tasks},
        )
        if not resp.get("success"):
            return SylvaSyncStatus(raw_response=resp)

        data = resp.get("data", {})
        return SylvaSyncStatus(
            files_parsed=data.get("filesParsed", 0),
            modules_total=data.get("modulesTotal", 0),
            theorems_total=data.get("theoremsTotal", 0),
            definitions_total=data.get("definitionsTotal", 0),
            sorry_total=data.get("sorryTotal", 0),
            axiom_total=data.get("axiomTotal", 0),
            millennium_problems=data.get("millenniumProblems", []),
            raw_response=resp,
        )

    def get_sylva_status(self) -> SylvaSyncStatus:
        """
        GET /api/research/sylva-sync
        获取当前同步状态（不触发重新同步）。
        """
        resp = self._make_request("GET", "/sylva-sync")
        if not resp.get("success"):
            return SylvaSyncStatus(raw_response=resp)

        data = resp.get("data", {})
        return SylvaSyncStatus(
            top_modules=data.get("topModules", []),
            active_research=data.get("activeResearch", []),
            recent_tasks=data.get("recentTasks", []),
            sync_history=data.get("syncHistory", []),
            raw_response=resp,
        )

    def get_modules(self, discipline: Optional[str] = None, status: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        GET /api/research/modules
        获取按 category 分组的模块列表。
        """
        params = []
        if discipline:
            params.append(f"discipline={discipline}")
        if status:
            params.append(f"status={status}")
        endpoint = "/modules"
        if params:
            endpoint += "?" + "&".join(params)

        resp = self._make_request("GET", endpoint)
        if not resp.get("success"):
            return {}
        return resp.get("data", {})

    def get_collaboration_templates(self) -> List[Dict[str, Any]]:
        """
        GET /api/research/collaborations/templates
        获取协作模板列表。
        """
        resp = self._make_request("GET", "/collaborations/templates")
        if not resp.get("success"):
            return []
        return resp.get("data", [])

    def init_millennium(self, topic: str) -> Dict[str, Any]:
        """
        POST /api/research/millennium/init
        初始化千年难题研究生态。
        """
        resp = self._make_request("POST", "/millennium/init", body={"topic": topic})
        return resp.get("data", {})

    def create_panel(self, topic: str, mode: str = "committee") -> Dict[str, Any]:
        """
        POST /api/research/panels
        创建学术专家组。
        """
        resp = self._make_request("POST", "/panels", body={"topic": topic, "mode": mode})
        return resp.get("data", {})

    def execute_panel(self, panel_id: str, prompt: str) -> Dict[str, Any]:
        """
        POST /api/research/panels/{id}/execute
        执行专家组审议。
        """
        resp = self._make_request("POST", f"/panels/{panel_id}/execute", body={"prompt": prompt})
        return resp.get("data", {})

    def generate_strategy_via_llm(self, req: LLMStrategyRequest) -> HeuristicStrategy:
        """
        通过千界花园的 LLM 服务生成工程策略。
        
        注意：千界花园本身不直接暴露 LLM 端点，而是通过协作接口调用。
        这里我们构造一个 task_force 类型的请求，让千界花园代表 PFE 调用 LLM。
        """
        # 构造 task_force 请求，描述为工程策略任务
        resp = self._make_request(
            "POST",
            "/collaborations/init",
            body={
                "type": req.collaboration_type,
                "topic": req.topic,
                "domain": req.domain,
                "mode": req.mode,
                "role": req.role,
                "specialty": req.specialty,
                "previousContent": req.previous_content,
                "targetModule": req.target_module,
                "targetPaper": req.target_paper,
            },
        )
        data = resp.get("data", {})
        content = data.get("content", data.get("response", data.get("result", "")))

        return HeuristicStrategy(
            name=f"QianJie-LLM-{req.collaboration_type}",
            description=content[:500] + ("..." if len(content) > 500 else ""),
            steps=[
                f"协作类型: {req.collaboration_type}",
                f"主题: {req.topic}",
                f"领域: {req.domain}",
            ],
            confidence=0.6 if content else 0.1,
            source="qianjie_llm",
            estimated_impact="提供工程方向性建议",
        )

    def push_verification_result(self, result: BridgeRunResult) -> Dict[str, Any]:
        """
        将 PFE 验证结果回传到千界花园。
        
        通过创建 ResearchNote 的方式记录。
        """
        report = result.report_markdown or self._generate_fallback_report(result)
        resp = self._make_request(
            "POST",
            "/notes",
            body={
                "title": f"PFE验证: {result.problem_name}",
                "content": report,
                "tags": ["pfe-bridge", result.problem_name, result.status.value],
                "priority": "high" if result.confidence_summary > 0.7 else "medium",
            },
        )
        return resp

    def _generate_fallback_report(self, result: BridgeRunResult) -> str:
        lines = [
            f"## PFE Bridge Result: {result.problem_name}",
            f"- Status: {result.status.value}",
            f"- Confidence: {result.confidence_summary:.2f}",
            f"- Time: {result.execution_time_ms}ms",
            "",
        ]
        for nr in result.numerical_results:
            lines.append(f"- {nr.target_name}: computed={nr.computed_value}, status={nr.status.value}")
        return "\n".join(lines)

    def health_check(self) -> Dict[str, Any]:
        """检查千界花园服务可用性。"""
        try:
            resp = self._make_request("GET", "/sylva-sync")
            return {
                "available": resp.get("success", False),
                "endpoint": self.config.base_url,
                "latency_ms": int((time.time() - self._last_request_time) * 1000),
                "response": resp.get("data", {}) if resp.get("success") else resp.get("error"),
            }
        except Exception as e:
            return {"available": False, "error": str(e)}


class QianJieBridge(PFEProblemBridge):
    """
    千界花园集成桥接器。

    继承 PFEProblemBridge 基类，为所有千年难题提供千界花园连接能力。
    每个具体的千年难题桥接（RiemannBridge, NavierStokesBridge 等）
    都可以包含一个 QianJieClient 实例，用于调用千界花园服务。
    """

    def __init__(self, problem_name: str, client: Optional[QianJieClient] = None, cache_dir: Optional[str] = None):
        super().__init__(problem_name, cache_dir)
        self.client = client or QianJieClient()
        self._sylva_status: Optional[SylvaSyncStatus] = None

    def verify_numerical(self, **kwargs) -> List[NumericalVerificationResult]:
        """委托给具体子类实现。"""
        raise NotImplementedError("QianJieBridge is a mixin; use concrete problem bridge")

    def generate_heuristic_strategy(self, context: Dict[str, Any]) -> List[HeuristicStrategy]:
        """通过千界花园 LLM 生成策略。"""
        req = LLMStrategyRequest(
            collaboration_type=context.get("collaboration_type", "task_force"),
            topic=context.get("topic", self.problem_name),
            domain=context.get("domain", "mathematics"),
            mode=context.get("mode", "engineering"),
            role=context.get("role", "PFE Engineer"),
            specialty=context.get("specialty", "numerical verification"),
            previous_content=context.get("previous_content", ""),
            target_module=context.get("target_module", ""),
            target_paper=context.get("target_paper", ""),
        )
        strategy = self.client.generate_strategy_via_llm(req)
        return [strategy]

    def confidence_assessment(self, numerical_results: List[NumericalVerificationResult],
                             strategies: List[HeuristicStrategy]) -> float:
        """综合评估：数值验证 + 千界花园策略质量。"""
        num_conf = self.compute_confidence_from_numerical(numerical_results)
        strat_conf = sum(s.confidence for s in strategies) / len(strategies) if strategies else 0.0
        # 加权：数值验证占 70%，策略质量占 30%
        return min(0.95, num_conf * 0.7 + strat_conf * 0.3)

    def translate_lean_to_python(self, lean_statement: str) -> Dict[str, Any]:
        """使用通用符号解析 + 千界花园元数据增强。"""
        symbols = self.parse_lean_symbols(lean_statement)
        # 尝试从千界花园获取相关模块信息
        modules = self.client.get_modules()
        related_module = None
        for cat, mods in modules.items():
            for m in mods:
                if self.problem_name.lower() in m.get("name", "").lower():
                    related_module = m
                    break

        return {
            "python_code": f"# PFE translation for: {self.problem_name}\n# Symbols: {symbols}\n# TODO: implement numerical equivalent",
            "symbols": symbols,
            "assumptions": ["PFE engineering approximation"],
            "computable": False,  # Millennium problems are not directly computable
            "related_module": related_module,
        }

    def run_pipeline(self, lean_context: Optional[Dict[str, Any]] = None) -> BridgeRunResult:
        """执行完整管道：获取状态 → 数值验证 → 策略生成 → 评估 → 回传。"""
        start = time.time()
        self._sylva_status = self.client.get_sylva_status()

        # 1. 数值验证（由子类实现）
        numerical_results = self.verify_numerical(**(lean_context or {}))

        # 2. 策略生成
        strategies = self.generate_heuristic_strategy(lean_context or {})

        # 3. 置信度评估
        confidence = self.confidence_assessment(numerical_results, strategies)

        # 4. 构建结果
        result = BridgeRunResult(
            problem_name=self.problem_name,
            status=BridgeStatus.PARTIAL if confidence > 0.3 else BridgeStatus.FAILED,
            numerical_results=numerical_results,
            strategies=strategies,
            confidence_summary=confidence,
            execution_time_ms=int((time.time() - start) * 1000),
            lean_translation=self.translate_lean_to_python(lean_context.get("lean_statement", "") if lean_context else ""),
        )

        # 5. 回传千界花园
        try:
            self.client.push_verification_result(result)
        except Exception as e:
            result.metadata["push_error"] = str(e)

        result.report_markdown = self.generate_markdown_report(result)
        return result

    def get_sylva_sync_status(self) -> SylvaSyncStatus:
        """获取 TOE-SYLVA 同步状态。"""
        if self._sylva_status is None:
            self._sylva_status = self.client.get_sylva_status()
        return self._sylva_status

    def find_high_sorry_modules(self, top_n: int = 3) -> List[Dict[str, Any]]:
        """从千界花园获取 sorry 最多的模块。"""
        status = self.get_sylva_sync_status()
        modules = sorted(
            status.top_modules,
            key=lambda m: m.get("sorryCount", 0),
            reverse=True,
        )
        return modules[:top_n]
