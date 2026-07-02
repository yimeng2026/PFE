#!/usr/bin/env python3
"""
pfe-bridges/qianjie_bridge.py — 千界花园后端桥接模块

连接 PFE 工程原型与千界花园 (Blooming Garden) 学术研究系统。
通过 HTTP API 调用千界花园的 research 服务，实现：
- 获取 TOE-SYLVA 状态同步
- 调用千界花园 LLM 进行工程策略生成
- 解析千界花园 JSON 数据
- 回传 PFE 验证结果

新增客户端（匹配千界花园实际 API 结构）：
- SylvaParserClient:  Python 移植 sylva-parser.ts 逻辑
- MillenniumInitClient: 封装 /api/research/millennium/init
- ResearchNoteClient:   封装 /api/research/notes (GET/POST/PUT/DELETE)
- AcademicPanelClient:  封装 /api/research/panels
- CollaborationInitClient: 封装 /api/research/collaborations/init

PFE ENGINEERING NOTE: 这是工程集成层，不追求形式化严格，
追求 PFE 与千界花园之间的有效数据涌现。
"""

import json
import re
import time
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

from .base_bridge import (
    PFEProblemBridge,
    BridgeStatus,
    NumericalVerificationResult,
    HeuristicStrategy,
    BridgeRunResult,
)


# ─── 配置与数据模型 ───

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
    collaboration_type: str
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


# ─── SylvaParserClient：Python 移植自 sylva-parser.ts ───

@dataclass
class LeanTheorem:
    """Lean 定理/引理/定义等结构（匹配 sylva-parser.ts 接口）。"""
    name: str
    type: str  # "theorem" | "lemma" | "def" | "axiom" | "conjecture" | "structure" | "inductive" | "instance"
    lineStart: int
    lineEnd: int
    statement: str
    proofStrategy: str
    hasSorry: bool
    sorryCount: int
    sorryLines: List[int]
    isMillennium: bool


@dataclass
class LeanModule:
    """解析后的 Lean 模块（匹配 sylva-parser.ts 接口）。"""
    fileName: str
    filePath: str
    totalLines: int
    theorems: List[LeanTheorem] = field(default_factory=list)
    definitions: List[LeanTheorem] = field(default_factory=list)
    sorryCount: int = 0
    todoCount: int = 0
    imports: List[str] = field(default_factory=list)
    namespace: str = ""
    moduleDescription: str = ""


@dataclass
class ParsedSYLVA:
    """解析整个 TOE-SYLVA 项目的结果（匹配 sylva-parser.ts 接口）。"""
    modules: List[LeanModule] = field(default_factory=list)
    totalTheorems: int = 0
    totalDefinitions: int = 0
    totalSorry: int = 0
    totalAxiom: int = 0
    millenniumProblems: List[Dict[str, Any]] = field(default_factory=list)
    todoItems: List[Dict[str, Any]] = field(default_factory=list)


class SylvaParserClient:
    """
    Python 移植自千界花园 sylva-parser.ts。

    提供纯文本解析（不依赖 lake/lean 编译），基于正则表达式和字符串模式匹配。
    可独立运行，无需千界花园服务在线。
    """

    # 定理/定义声明模式
    THEOREM_PATTERN = re.compile(r"^(theorem|lemma|def|axiom|conjecture|structure|inductive|instance)\s+(\S+)")
    DOC_PATTERN = re.compile(r"^\/-+?\s*(.*)")

    def parse_lean_file(self, file_path: str, content: str) -> LeanModule:
        """解析单个 Lean 文件（匹配 sylva-parser.ts 的 parseLeanFile）。"""
        lines = content.split("\n")
        file_name = Path(file_path).name

        module = LeanModule(
            fileName=file_name,
            filePath=file_path,
            totalLines=len(lines),
            theorems=[],
            definitions=[],
            sorryCount=0,
            todoCount=0,
            imports=[],
            namespace="",
            moduleDescription="",
        )

        # 提取文件描述（顶部注释）
        description_lines: List[str] = []
        i = 0
        while i < len(lines):
            trimmed = lines[i].strip()
            if trimmed.startswith("/-") or trimmed == "-/" or trimmed == "":
                i += 1
                continue
            if trimmed.startswith("-"):
                description_lines.append(trimmed.lstrip("- ").strip())
                i += 1
            else:
                break
        module.moduleDescription = " ".join(description_lines).strip()

        # 提取 imports
        for line in lines:
            import_match = re.match(r"^import\s+(.+)$", line)
            if import_match:
                module.imports.append(import_match.group(1).strip())
            namespace_match = re.match(r"^namespace\s+(\S+)", line)
            if namespace_match:
                module.namespace = namespace_match.group(1)

        # 解析 theorem / lemma / def / axiom / conjecture / structure / inductive / instance
        blocks: List[Dict[str, Any]] = []
        current_block: Optional[Dict[str, Any]] = None

        for line_idx, line in enumerate(lines):
            trimmed = line.strip()

            # 定理/定义声明开始
            match = self.THEOREM_PATTERN.match(trimmed)
            if match:
                if current_block is not None:
                    blocks.append(current_block)
                current_block = {
                    "name": match.group(2),
                    "type": match.group(1),
                    "lineStart": line_idx + 1,
                    "lines": [line],
                    "docLines": [],
                }
                continue

            # 文档注释
            doc_match = self.DOC_PATTERN.match(trimmed)
            if doc_match and current_block is not None:
                current_block["docLines"].append(doc_match.group(1))
                continue

            # 收集 block 内容
            if current_block is not None:
                current_block["lines"].append(line)
                if trimmed.startswith("end "):
                    blocks.append(current_block)
                    current_block = None

        if current_block is not None:
            blocks.append(current_block)

        # 后处理：精确划分 block 边界，提取 sorry 与 proofStrategy
        finalized_theorems: List[LeanTheorem] = []
        for block in blocks:
            block_lines = block["lines"]
            end_line = block["lineStart"] + len(block_lines) - 1

            # 重新计算精确结束位置（找到下一个顶行声明或 end）
            for j in range(block["lineStart"] - 1 + len(block_lines), len(lines)):
                l = lines[j]
                if l.strip() == "":
                    continue
                if not l.startswith(" ") and not l.startswith("\t"):
                    if self.THEOREM_PATTERN.match(l.strip()) or l.strip().startswith("end "):
                        end_line = j
                        break

            actual_block = lines[block["lineStart"] - 1:end_line]
            sorry_lines: List[int] = []
            proof_strategy = ""

            for k, actual_line in enumerate(actual_block):
                if re.search(r"\bsorry\b", actual_line):
                    sorry_lines.append(block["lineStart"] + k)
                    # 向前查找注释（匹配 sylva-parser.ts 逻辑：最多前5行）
                    for m in range(k - 1, max(-1, k - 5), -1):
                        if m < 0:
                            break
                        prev_line = actual_block[m].strip()
                        if prev_line.startswith("--"):
                            proof_strategy = prev_line.lstrip("- ").strip() + " " + proof_strategy
                        elif prev_line == "" or prev_line.startswith("·"):
                            continue
                        else:
                            break

            is_millennium = bool(
                re.search(r"Millennium\s*(Prize)?\s*(Problem|Problems)", "\n".join(block_lines), re.I)
                or re.search(r"Clay\s*Mathematics", "\n".join(block_lines), re.I)
                or re.search(r"千年\s*难题", "\n".join(block_lines))
            )

            theorem = LeanTheorem(
                name=block["name"],
                type=block["type"],
                lineStart=block["lineStart"],
                lineEnd=end_line,
                statement=self._extract_statement(actual_block),
                proofStrategy=proof_strategy.strip(),
                hasSorry=len(sorry_lines) > 0,
                sorryCount=len(sorry_lines),
                sorryLines=sorry_lines,
                isMillennium=is_millennium,
            )
            finalized_theorems.append(theorem)

        module.theorems = finalized_theorems
        module.sorryCount = sum(t.sorryCount for t in module.theorems)

        # 分离 definitions（type 为 def / structure / inductive / instance）
        module.definitions = [t for t in module.theorems if t.type in ("def", "structure", "inductive", "instance")]
        module.theorems = [t for t in module.theorems if t.type in ("theorem", "lemma", "axiom", "conjecture")]

        return module

    def _extract_statement(self, block_lines: List[str]) -> str:
        """提取声明部分（:= by 之前的文本），匹配 sylva-parser.ts 的 extractStatement。"""
        full_text = "\n".join(block_lines)
        by_match = re.search(r"(?::=\s*by\b)", full_text)
        if by_match:
            return full_text[:by_match.start()].strip()
        where_match = re.search(r"(?::=\s*\{)", full_text)
        if where_match:
            return full_text[:where_match.start()].strip()
        simple_match = re.search(r"(?::=\s*)", full_text)
        if simple_match:
            return full_text[:simple_match.start()].strip()
        return full_text[:min(300, len(full_text))].strip()

    def extract_todos(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """从 Lean 代码中提取 TODO(research) 项（匹配 sylva-parser.ts 的 extractTODOs）。"""
        lines = content.split("\n")
        todos: List[Dict[str, Any]] = []
        for i, line in enumerate(lines):
            match = re.search(r"TODO\(research\)[\s:]?(.*)", line, re.I)
            if match:
                todos.append({
                    "filePath": file_path,
                    "line": i + 1,
                    "content": match.group(1).strip(),
                })
        return todos

    def parse_sylva_project(self, files: List[Dict[str, str]]) -> ParsedSYLVA:
        """解析整个 TOE-SYLVA 项目的 Lean 文件（匹配 sylva-parser.ts 的 parseSYLVAProject）。"""
        result = ParsedSYLVA()

        for file in files:
            if not file["path"].endswith(".lean"):
                continue
            module = self.parse_lean_file(file["path"], file["content"])
            result.modules.append(module)
            result.totalTheorems += len(module.theorems)
            result.totalDefinitions += len(module.definitions)
            result.totalSorry += module.sorryCount
            result.totalAxiom += len([t for t in module.theorems if t.type == "axiom"])

            for t in module.theorems:
                if t.isMillennium or t.type == "axiom":
                    result.millenniumProblems.append({
                        "name": t.name,
                        "filePath": module.filePath,
                        "line": t.lineStart,
                        "type": "axiom" if t.type == "axiom" else "conjecture" if t.type == "conjecture" else "theorem",
                    })

            result.todoItems.extend(self.extract_todos(file["path"], file["content"]))

        return result

    def generate_module_sync_data(self, module: LeanModule) -> Dict[str, Any]:
        """生成 ResearchModule 同步数据（匹配 sylva-parser.ts 的 generateModuleSyncData）。"""
        discipline = "mathematics"
        fp = module.filePath
        if "Hodge" in fp:
            discipline = "algebraic_geometry"
        elif "NavierStokes" in fp:
            discipline = "pde"
        elif "Complexity" in fp:
            discipline = "computational_complexity"
        elif "Riemann" in fp:
            discipline = "number_theory"

        return {
            "name": module.fileName.replace(".lean", ""),
            "displayName": module.fileName,
            "category": "Millennium_Problem",
            "subcategory": module.namespace or "sylva",
            "discipline": discipline,
            "lineCount": module.totalLines,
            "sorryCount": module.sorryCount,
            "theoremCount": len(module.theorems),
            "definitionCount": len(module.definitions),
            "filePath": module.filePath,
            "dependencies": json.dumps(module.imports),
        }

    def generate_theorem_sync_data(self, theorem: LeanTheorem, module_id: str) -> Dict[str, Any]:
        """生成 ResearchTheorem 同步数据（匹配 sylva-parser.ts 的 generateTheoremSyncData）。"""
        status = "axiom" if theorem.type == "axiom" else "research" if theorem.hasSorry else "proven"
        return {
            "name": theorem.name,
            "statement": theorem.statement,
            "moduleId": module_id,
            "status": status,
            "proofStrategy": theorem.proofStrategy,
            "leanCode": f"{theorem.name} ({theorem.type}): {theorem.statement}",
        }

    def generate_task_for_sorry(
        self,
        theorem: LeanTheorem,
        module_name: str,
        workshop_id: Optional[str] = None,
        pipeline_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """生成 AcademicTask 同步数据（匹配 sylva-parser.ts 的 generateTaskForSorry）。"""
        priority = "critical" if theorem.isMillennium else "high" if theorem.sorryCount > 3 else "normal"
        return {
            "title": f"证明 {theorem.name} ({theorem.sorryCount} 个 sorry)",
            "description": (
                f"模块 {module_name} 中的定理 {theorem.name} 需要完成 {theorem.sorryCount} 个 sorry 的证明。"
                + (f" 已知策略: {theorem.proofStrategy}" if theorem.proofStrategy else "")
                + (" [Millennium Problem]" if theorem.isMillennium else "")
            ),
            "type": "verify" if theorem.type == "axiom" else "prove",
            "status": "pending",
            "priority": priority,
            "targetModule": module_name,
            "targetPaper": theorem.name,
            "workshopId": workshop_id,
            "pipelineId": pipeline_id,
        }

    def generate_sorry_analysis_prompt(self, theorem: LeanTheorem, module_description: str) -> str:
        """生成 LLM 分析提示词（匹配 sylva-parser.ts 的 generateSorryAnalysisPrompt）。"""
        return (
            f"请分析以下 Lean 4 定理中的 sorry，并提供详细的证明策略：\n\n"
            f"**定理**: {theorem.name}\n"
            f"**类型**: {theorem.type}\n"
            f"**模块描述**: {module_description}\n"
            f"**已有策略注释**: {theorem.proofStrategy or '无'}\n\n"
            f"**定理声明**:\n{theorem.statement}\n\n"
            f"**sorry 数量**: {theorem.sorryCount}\n\n"
            f"请提供：\n"
            f"1. 该定理的数学背景解释\n"
            f"2. 每个 sorry 对应的证明步骤\n"
            f"3. 建议使用的 Lean 4 tactics\n"
            f"4. 相关数学定理/引理的引用\n"
            f"5. 证明难度评估（1-10）\n\n"
            f"请以结构化格式输出。"
        )

    def health_check(self) -> Dict[str, Any]:
        """检查 SylvaParserClient 可用性（通过解析一个示例片段）。"""
        try:
            sample = (
                "theorem test_add : 1 + 1 = 2 := by\n"
                "  -- 使用 rfl 策略\n"
                "  sorry\n"
            )
            module = self.parse_lean_file("test.lean", sample)
            return {
                "available": True,
                "parser": "sylva-parser-python",
                "sample_parsed": len(module.theorems) == 1 and module.theorems[0].hasSorry,
                "version": "1.0.0",
            }
        except Exception as e:
            return {"available": False, "error": str(e), "parser": "sylva-parser-python", "fallback": True}


# ─── BaseHTTPClient：通用 HTTP 客户端（零外部依赖） ───

class BaseHTTPClient:
    """
    基于 urllib.request 的通用 HTTP 客户端，零外部依赖。

    所有子客户端继承此类，默认连接到 localhost:3000。
    包含详细的错误处理和 fallback 数据返回。
    """

    def __init__(
        self,
        base_url: str = "http://localhost:3000",
        api_prefix: str = "/api/research",
        timeout: int = 30,
        max_retries: int = 2,
        retry_delay: float = 1.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_prefix = api_prefix
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._last_request_time: float = 0.0
        self._min_interval: float = 0.5

    def _make_request(
        self,
        method: str,
        endpoint: str,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """发送 HTTP 请求并返回 JSON 响应，包含详细的错误处理和 fallback 数据。"""
        url = f"{self.base_url}{self.api_prefix}{endpoint}"
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

        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                self._last_request_time = time.time()
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                last_error = e
                if e.code in (429, 500, 502, 503) and attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                    continue
                try:
                    body_text = e.read().decode("utf-8")
                    return json.loads(body_text)
                except Exception:
                    return {
                        "success": False,
                        "error": f"HTTP {e.code}: {e.reason}",
                        "fallback": True,
                    }
            except urllib.error.URLError as e:
                last_error = e
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                    continue
                return {
                    "success": False,
                    "error": f"Connection error: {e.reason}",
                    "fallback": True,
                }
            except Exception as e:
                last_error = e
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                    continue
                return {
                    "success": False,
                    "error": str(e),
                    "fallback": True,
                }

        return {
            "success": False,
            "error": str(last_error) if last_error else "Unknown error",
            "fallback": True,
        }

    def health_check(self) -> Dict[str, Any]:
        """检查服务端可用性。子类应覆盖以调用具体端点。"""
        try:
            resp = self._make_request("GET", "/sylva-sync")
            return {
                "available": resp.get("success", False),
                "endpoint": self.base_url,
                "latency_ms": int((time.time() - self._last_request_time) * 1000),
                "response": resp.get("data", {}) if resp.get("success") else resp.get("error"),
                "fallback": resp.get("fallback", False),
            }
        except Exception as e:
            return {"available": False, "error": str(e), "fallback": True}


# ─── MillenniumInitClient：封装 /api/research/millennium/init ───

class MillenniumInitClient(BaseHTTPClient):
    """封装千界花园 /api/research/millennium/init 端点。"""

    def init(self) -> Dict[str, Any]:
        """POST /api/research/millennium/init — 初始化千年难题研究生态。"""
        resp = self._make_request("POST", "/millennium/init")
        return resp

    def get_status(self) -> Dict[str, Any]:
        """GET /api/research/millennium/init — 获取千年难题研究生态状态。"""
        resp = self._make_request("GET", "/millennium/init")
        return resp

    def health_check(self) -> Dict[str, Any]:
        """检查 millennium/init 端点可用性。"""
        resp = self.get_status()
        return {
            "available": resp.get("success", False),
            "endpoint": f"{self.base_url}{self.api_prefix}/millennium/init",
            "response": resp.get("data", {}) if resp.get("success") else resp.get("error"),
            "fallback": resp.get("fallback", False),
        }


# ─── ResearchNoteClient：封装 /api/research/notes ───

class ResearchNoteClient(BaseHTTPClient):
    """封装千界花园 /api/research/notes 端点（GET/POST/PUT/DELETE）。"""

    def get_notes(self, tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """GET /api/research/notes — 获取研究笔记，支持按 tag 筛选。"""
        endpoint = "/notes"
        if tag:
            endpoint += f"?tag={urllib.parse.quote(tag)}"
        resp = self._make_request("GET", endpoint)
        return resp.get("data", []) if resp.get("success") else []

    def create_note(
        self,
        title: str,
        content: str = "",
        tags: Optional[List[str]] = None,
        moduleId: Optional[str] = None,
        paperId: Optional[str] = None,
    ) -> Dict[str, Any]:
        """POST /api/research/notes — 创建研究笔记。"""
        if not title or not title.strip():
            return {"success": False, "error": "Title is required", "fallback": True}
        resp = self._make_request(
            "POST",
            "/notes",
            body={
                "title": title.strip(),
                "content": content or "",
                "tags": tags or [],
                "moduleId": moduleId,
                "paperId": paperId,
            },
        )
        return resp

    def update_note(
        self,
        id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        moduleId: Optional[str] = None,
        paperId: Optional[str] = None,
    ) -> Dict[str, Any]:
        """PUT /api/research/notes — 更新研究笔记。"""
        if not id:
            return {"success": False, "error": "ID is required", "fallback": True}
        body: Dict[str, Any] = {"id": id}
        if title is not None:
            body["title"] = title.strip()
        if content is not None:
            body["content"] = content
        if tags is not None:
            body["tags"] = tags
        if moduleId is not None:
            body["moduleId"] = moduleId or None
        if paperId is not None:
            body["paperId"] = paperId or None
        resp = self._make_request("PUT", "/notes", body=body)
        return resp

    def delete_note(self, id: str) -> Dict[str, Any]:
        """DELETE /api/research/notes — 删除研究笔记。"""
        if not id:
            return {"success": False, "error": "ID is required", "fallback": True}
        resp = self._make_request("DELETE", "/notes", body={"id": id})
        return resp

    def health_check(self) -> Dict[str, Any]:
        """检查 notes 端点可用性（通过 GET 请求）。"""
        resp = self._make_request("GET", "/notes")
        return {
            "available": resp.get("success", False),
            "endpoint": f"{self.base_url}{self.api_prefix}/notes",
            "response": resp.get("data", []) if resp.get("success") else resp.get("error"),
            "fallback": resp.get("fallback", False),
        }


# ─── AcademicPanelClient：封装 /api/research/panels ───

class AcademicPanelClient(BaseHTTPClient):
    """封装千界花园 /api/research/panels 端点。"""

    def get_panels(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """GET /api/research/panels — 获取专家组列表，支持 domain 筛选。"""
        endpoint = "/panels"
        if domain:
            endpoint += f"?domain={urllib.parse.quote(domain)}"
        resp = self._make_request("GET", endpoint)
        return resp.get("data", []) if resp.get("success") else []

    def create_panel(
        self,
        name: str,
        description: str = "",
        domain: str = "interdisciplinary",
        strategy: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """POST /api/research/panels — 创建学术专家组。"""
        if not name or not name.strip():
            return {
                "success": False,
                "error": "Panel name is required",
                "fallback": True,
            }
        body = {
            "name": name.strip(),
            "description": description or "",
            "domain": domain,
            "strategy": strategy or {},
        }
        resp = self._make_request("POST", "/panels", body=body)
        return resp

    def health_check(self) -> Dict[str, Any]:
        """检查 panels 端点可用性（通过 GET 请求）。"""
        resp = self._make_request("GET", "/panels")
        return {
            "available": resp.get("success", False),
            "endpoint": f"{self.base_url}{self.api_prefix}/panels",
            "response": resp.get("data", []) if resp.get("success") else resp.get("error"),
            "fallback": resp.get("fallback", False),
        }


# ─── CollaborationInitClient：封装 /api/research/collaborations/init ───

class CollaborationInitClient(BaseHTTPClient):
    """封装千界花园 /api/research/collaborations/init 端点。"""

    VALID_TYPES = (
        "full_research",
        "theorem_proving",
        "paper_writing",
        "peer_review",
        "educational",
    )

    def init_collaboration(self, domain: str, topic: str, collaboration_type: str) -> Dict[str, Any]:
        """POST /api/research/collaborations/init — 初始化协作生态。"""
        if not domain or not topic or not collaboration_type:
            return {
                "success": False,
                "error": "domain, topic, and collaborationType are required",
                "fallback": True,
            }
        if collaboration_type not in self.VALID_TYPES:
            return {
                "success": False,
                "error": f"Invalid collaborationType. Valid: {', '.join(self.VALID_TYPES)}",
                "fallback": True,
            }
        resp = self._make_request(
            "POST",
            "/collaborations/init",
            body={
                "domain": domain,
                "topic": topic,
                "collaborationType": collaboration_type,
            },
        )
        return resp

    def health_check(self) -> Dict[str, Any]:
        """检查 collaborations/init 端点可用性。"""
        resp = self._make_request(
            "POST",
            "/collaborations/init",
            body={
                "domain": "mathematics",
                "topic": "health-check",
                "collaborationType": "educational",
            },
        )
        return {
            "available": resp.get("success", False),
            "endpoint": f"{self.base_url}{self.api_prefix}/collaborations/init",
            "response": resp.get("data", {}) if resp.get("success") else resp.get("error"),
            "fallback": resp.get("fallback", False),
        }


# ─── QianJieClient（保留并增强，兼容现有代码） ───

class QianJieClient:
    """
    千界花园 HTTP API 聚合客户端。

    封装对千界花园 /api/research/* 端点的调用，提供：
    - GET/POST 通用请求
    - 错误重试
    - JSON 解析
    - 响应缓存
    - 子客户端访问（parser, millennium, notes, panels, collaborations）
    """

    def __init__(self, config: Optional[QianJieConfig] = None):
        self.config = config or QianJieConfig()
        self._cache: Dict[str, Any] = {}
        self._last_request_time: float = 0.0
        self._min_interval: float = 0.5

        # 子客户端实例（新增）
        self.parser = SylvaParserClient()
        self.millennium = MillenniumInitClient(
            base_url=self.config.base_url,
            api_prefix=self.config.api_prefix,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries,
            retry_delay=self.config.retry_delay,
        )
        self.notes = ResearchNoteClient(
            base_url=self.config.base_url,
            api_prefix=self.config.api_prefix,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries,
            retry_delay=self.config.retry_delay,
        )
        self.panels = AcademicPanelClient(
            base_url=self.config.base_url,
            api_prefix=self.config.api_prefix,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries,
            retry_delay=self.config.retry_delay,
        )
        self.collaborations = CollaborationInitClient(
            base_url=self.config.base_url,
            api_prefix=self.config.api_prefix,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries,
            retry_delay=self.config.retry_delay,
        )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """发送 HTTP 请求并返回 JSON 响应（保留向后兼容）。"""
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

    # ─── 向后兼容的 API 封装 ───

    def sync_sylva(self, analyze_with_llm: bool = True, create_tasks: bool = True) -> SylvaSyncStatus:
        """POST /api/research/sylva-sync — 触发 TOE-SYLVA 同步。"""
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
        """GET /api/research/sylva-sync — 获取当前同步状态。"""
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

    def get_modules(
        self, discipline: Optional[str] = None, status: Optional[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """GET /api/research/modules — 获取按 category 分组的模块列表。"""
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
        """GET /api/research/collaborations/templates — 获取协作模板列表。"""
        resp = self._make_request("GET", "/collaborations/templates")
        if not resp.get("success"):
            return []
        return resp.get("data", [])

    def init_millennium(self, topic: str) -> Dict[str, Any]:
        """POST /api/research/millennium/init — 初始化千年难题研究生态。"""
        resp = self._make_request("POST", "/millennium/init", body={"topic": topic})
        return resp.get("data", {})

    def create_panel(self, topic: str, mode: str = "committee") -> Dict[str, Any]:
        """POST /api/research/panels — 创建学术专家组。"""
        resp = self._make_request("POST", "/panels", body={"topic": topic, "mode": mode})
        return resp.get("data", {})

    def execute_panel(self, panel_id: str, prompt: str) -> Dict[str, Any]:
        """POST /api/research/panels/{id}/execute — 执行专家组审议。"""
        resp = self._make_request("POST", f"/panels/{panel_id}/execute", body={"prompt": prompt})
        return resp.get("data", {})

    def generate_strategy_via_llm(self, req: LLMStrategyRequest) -> HeuristicStrategy:
        """通过千界花园的 LLM 服务生成工程策略。"""
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
        """将 PFE 验证结果回传到千界花园（通过 ResearchNote）。"""
        report = result.report_markdown or self._generate_fallback_report(result)
        resp = self._make_request(
            "POST",
            "/notes",
            body={
                "title": f"PFE验证: {result.problem_name}",
                "content": report,
                "tags": ["pfe-bridge", result.problem_name, result.status.value],
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


# ─── QianJieBridge（保留） ───

class QianJieBridge(PFEProblemBridge):
    """
    千界花园集成桥接器。

    继承 PFEProblemBridge 基类，为所有千年难题提供千界花园连接能力。
    每个具体的千年难题桥接（RiemannBridge, NavierStokesBridge 等）
    都可以包含一个 QianJieClient 实例，用于调用千界花园服务。
    """

    def __init__(
        self,
        problem_name: str,
        client: Optional[QianJieClient] = None,
        cache_dir: Optional[str] = None,
    ):
        super().__init__(problem_name, cache_dir, qianjie_client=client or QianJieClient())
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

    def confidence_assessment(
        self,
        numerical_results: List[NumericalVerificationResult],
        strategies: List[HeuristicStrategy],
    ) -> float:
        """综合评估：数值验证 + 千界花园策略质量。"""
        num_conf = self.compute_confidence_from_numerical(numerical_results)
        strat_conf = sum(s.confidence for s in strategies) / len(strategies) if strategies else 0.0
        # 加权：数值验证占 70%，策略质量占 30%
        return min(0.95, num_conf * 0.7 + strat_conf * 0.3)

    def translate_lean_to_python(self, lean_statement: str) -> Dict[str, Any]:
        """使用通用符号解析 + 千界花园元数据增强。"""
        symbols = self.parse_lean_symbols(lean_statement)
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
            "computable": False,
            "related_module": related_module,
        }

    def run_pipeline(self, lean_context: Optional[Dict[str, Any]] = None) -> BridgeRunResult:
        """执行完整管道：获取状态 → 数值验证 → 策略生成 → 评估 → 回传。"""
        start = time.time()
        self._sylva_status = self.client.get_sylva_status()

        numerical_results = self.verify_numerical(**(lean_context or {}))
        strategies = self.generate_heuristic_strategy(lean_context or {})
        confidence = self.confidence_assessment(numerical_results, strategies)

        result = BridgeRunResult(
            problem_name=self.problem_name,
            status=BridgeStatus.PARTIAL if confidence > 0.3 else BridgeStatus.FAILED,
            numerical_results=numerical_results,
            strategies=strategies,
            confidence_summary=confidence,
            execution_time_ms=int((time.time() - start) * 1000),
            lean_translation=self.translate_lean_to_python(
                lean_context.get("lean_statement", "") if lean_context else ""
            ),
        )

        try:
            self.push_to_qianjie(result)
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
