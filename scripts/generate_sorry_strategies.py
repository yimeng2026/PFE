#!/usr/bin/env python3
"""
generate_sorry_strategies.py — Zhipu GLM-5.1 策略生成脚本 for TOE-SYLVA sorry

功能：
1. 递归读取 TOE-SYLVA 的 Lean 文件
2. 提取所有包含 sorry 的 theorem/lemma/def/axiom/conjecture
3. 提取其前的 PFE ENGINEERING NOTE / STRATEGY / LEMMAS NEEDED / TACTICS NEEDED 注释
4. 构建提示词，调用 Zhipu GLM-5.1 API 生成详细证明策略
5. 输出 Markdown 报告到 reports/sorry_strategies_YYYYMMDD.md

调用方式：
  python scripts/generate_sorry_strategies.py [--sylva-dir PATH] [--output-dir PATH] [--max-sorry N]

PFE ENGINEERING NOTE: 零外部依赖（仅 urllib），追求有效涌现。
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional

# ─── 常量 ───
TOE_SYLVA_DEFAULT = r"C:\Users\一梦\Documents\TOE-SYLVA-pull"
ZHIPU_ENDPOINT = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
ZHIPU_MODEL = "glm-5.1"
ZHIPU_TEMPERATURE = 0.3
ZHIPU_MAX_TOKENS = 4096


# ─── 数据类 ───

@dataclass
class SorryEntry:
    """单个 sorry 的完整记录。"""
    theorem_name: str
    file_path: str
    line_number: int
    theorem_type: str  # theorem / lemma / def / axiom / conjecture
    statement: str
    existing_strategy: str = ""
    existing_lemmas: str = ""
    existing_tactics: str = ""
    engineering_note: str = ""
    strategy: str = ""
    difficulty: int = 5
    suggested_lemmas: List[str] = field(default_factory=list)
    suggested_tactics: List[str] = field(default_factory=list)
    confidence: float = 0.0
    llm_response: str = ""
    llm_latency_ms: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SorryReport:
    """完整报告。"""
    generated_at: str
    total_files: int
    total_theorems: int
    total_sorry: int
    entries: List[SorryEntry]
    api_errors: List[str] = field(default_factory=list)


# ─── Lean 解析器 ───

class LeanParser:
    """
    千界花园 sylva-parser.ts 的 Python 移植。
    纯正则解析，不依赖 lake/lean 编译。
    """

    THEOREM_PATTERN = re.compile(
        r'^(theorem|lemma|def|axiom|conjecture|structure|inductive|instance)\s+'
        r'([a-zA-Z_][a-zA-Z0-9_\']*)'
    )
    SORRY_PATTERN = re.compile(r'\bsorry\b')
    COMMENT_PATTERN = re.compile(r'^\s*--\s*(.*)$')
    ENGINEERING_NOTE = re.compile(r'PFE ENGINEERING NOTE[:\s]*(.*)', re.IGNORECASE)
    STRATEGY = re.compile(r'\[?STRATEGY\]?[:\s]*(.*)', re.IGNORECASE)
    LEMMAS_NEEDED = re.compile(r'LEMMAS NEEDED[:\s]*(.*)', re.IGNORECASE)
    TACTICS_NEEDED = re.compile(r'TACTICS NEEDED[:\s]*(.*)', re.IGNORECASE)
    IMPORT_PATTERN = re.compile(r'^import\s+(.+)')
    NAMESPACE_PATTERN = re.compile(r'^namespace\s+(\S+)')

    def __init__(self, lean_dir: str):
        self.lean_dir = Path(lean_dir)
        self.modules: List[Dict[str, Any]] = []

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        module = {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'total_lines': len(lines),
            'theorems': [],
            'definitions': [],
            'axioms': [],
            'sorry_count': 0,
            'imports': [],
            'namespace': '',
            'description': ''
        }

        # 提取文件顶部注释
        desc_lines = []
        for line in lines[:20]:
            stripped = line.strip()
            if stripped.startswith('-') or stripped.startswith('/'):
                desc_lines.append(stripped.lstrip('-/').strip())
            elif stripped and not stripped.startswith('import'):
                break
        module['description'] = ' '.join(desc_lines)[:200]

        # 解析 imports 和 namespace
        for line in lines:
            if m := self.IMPORT_PATTERN.match(line.strip()):
                module['imports'].append(m.group(1).strip())
            if m := self.NAMESPACE_PATTERN.match(line.strip()):
                module['namespace'] = m.group(1)

        # 逐行解析 theorem / lemma / def / axiom / conjecture
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            m = self.THEOREM_PATTERN.match(stripped)
            if m:
                decl_type = m.group(1)
                decl_name = m.group(2)
                start_line = i + 1

                # 收集 block 直到下一个同层级声明或 end
                block_lines = [line]
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    next_stripped = next_line.strip()
                    # block 结束检测
                    if next_stripped.startswith('end ') or next_stripped == 'end':
                        break
                    if self.THEOREM_PATTERN.match(next_stripped):
                        # 检查缩进：如果新声明不缩进且不是当前 block 的一部分
                        if not next_line.startswith(' ') and not next_line.startswith('\t'):
                            break
                    block_lines.append(next_line)
                    j += 1
                i = j - 1  # 外循环会 i+=1，所以这里 -1

                block_text = '\n'.join(block_lines)
                has_sorry = bool(self.SORRY_PATTERN.search(block_text))
                sorry_lines_in_block = []
                for k, bl in enumerate(block_lines):
                    if self.SORRY_PATTERN.search(bl):
                        sorry_lines_in_block.append(start_line + k)

                # 提取 block 前的注释（最多向上看 10 行）
                pre_comments = []
                lookback_start = max(0, start_line - 11)
                for k in range(lookback_start, start_line - 1):
                    cm = self.COMMENT_PATTERN.match(lines[k])
                    if cm:
                        pre_comments.append(cm.group(1))

                # 提取特定注释类型
                engineering_note = ""
                strategy = ""
                lemmas_needed = ""
                tactics_needed = ""
                for comment in pre_comments:
                    if em := self.ENGINEERING_NOTE.search(comment):
                        engineering_note = em.group(1).strip()
                    if sm := self.STRATEGY.search(comment):
                        strategy = sm.group(1).strip()
                    if lm := self.LEMMAS_NEEDED.search(comment):
                        lemmas_needed = lm.group(1).strip()
                    if tm := self.TACTICS_NEEDED.search(comment):
                        tactics_needed = tm.group(1).strip()

                # 提取声明语句（:= by 之前的部分）
                statement = self._extract_statement(block_lines)

                decl = {
                    'name': decl_name,
                    'type': decl_type,
                    'line': start_line,
                    'has_sorry': has_sorry,
                    'sorry_count': len(sorry_lines_in_block),
                    'sorry_lines': sorry_lines_in_block,
                    'statement': statement,
                    'engineering_note': engineering_note,
                    'strategy': strategy,
                    'lemmas_needed': lemmas_needed,
                    'tactics_needed': tactics_needed,
                }

                if decl_type in ('theorem', 'lemma'):
                    module['theorems'].append(decl)
                elif decl_type == 'def':
                    module['definitions'].append(decl)
                elif decl_type == 'axiom':
                    module['axioms'].append(decl)
            i += 1

        module['sorry_count'] = sum(
            t['sorry_count'] for t in module['theorems']
        ) + sum(
            t['sorry_count'] for t in module['definitions']
        ) + sum(
            t['sorry_count'] for t in module['axioms']
        )
        return module

    def _extract_statement(self, block_lines: List[str]) -> str:
        full_text = '\n'.join(block_lines)
        # 尝试找到 := by 或 := { 之前的部分
        for pattern in [r'(:=\s*by\b)', r'(:=\s*\{)', r'(:=\s*)']:
            m = re.search(pattern, full_text)
            if m:
                return full_text[:m.start()].strip()[:300]
        return full_text[:300].strip()

    def _should_skip(self, path: Path) -> bool:
        """判断是否应该跳过该路径。"""
        p = str(path)
        skip_patterns = [
            '.lake', 'lake-packages', 'archive', 'sylva_formalization',
            '.git', 'node_modules', '__pycache__', '.pfe-bridge-cache',
        ]
        return any(pat in p for pat in skip_patterns)

    def parse_all(self) -> List[Dict[str, Any]]:
        for lean_file in self.lean_dir.rglob('*.lean'):
            if self._should_skip(lean_file):
                continue
            try:
                module = self.parse_file(lean_file)
                self.modules.append(module)
            except Exception as e:
                print(f"[Warning] Failed to parse {lean_file}: {e}")
        return self.modules


# ─── Zhipu API 调用 ───

def get_zhipu_api_key() -> Optional[str]:
    for key in ['ZHIPU_API_KEY', 'GLM51_API_KEY_1', 'GLM_API_KEY']:
        val = os.environ.get(key)
        if val:
            return val
    return None


def call_zhipu_glm51(prompt: str, system_prompt: str = "") -> Dict[str, Any]:
    """
    调用 Zhipu GLM-5.1 API。
    返回 dict: {content, reasoning, usage, latency_ms, error}
    """
    api_key = get_zhipu_api_key()
    if not api_key:
        return {"error": "No ZHIPU_API_KEY found in environment", "content": "", "latency_ms": 0}

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    body = {
        "model": ZHIPU_MODEL,
        "messages": messages,
        "temperature": ZHIPU_TEMPERATURE,
        "max_tokens": ZHIPU_MAX_TOKENS,
    }

    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(
        ZHIPU_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode('utf-8')
        except Exception:
            err_body = str(e)
        return {"error": f"HTTP {e.code}: {err_body}", "content": "", "latency_ms": int((time.time() - start) * 1000)}
    except Exception as e:
        return {"error": str(e), "content": "", "latency_ms": int((time.time() - start) * 1000)}

    latency_ms = int((time.time() - start) * 1000)
    choice = result.get("choices", [{}])[0]
    message = choice.get("message", {})
    content = message.get("content", "")
    reasoning = message.get("reasoning", "")
    usage = result.get("usage", {})

    return {
        "content": content,
        "reasoning": reasoning,
        "usage": usage,
        "latency_ms": latency_ms,
        "error": None,
    }


def fallback_strategy(entry: SorryEntry) -> None:
    """API 不可用时的本地启发式策略回退。"""
    entry.strategy = (
        f"【本地回退策略】基于已有注释的启发式推断。\n"
        f"已有策略: {entry.existing_strategy}\n"
        f"建议引理: {entry.existing_lemmas}\n"
        f"建议策略: {entry.existing_tactics}\n"
        f"\n请检查 Mathlib 中是否有相关引理，并尝试使用 simp / rw / apply 组合。"
    )
    entry.difficulty = 5
    entry.suggested_lemmas = [l.strip() for l in entry.existing_lemmas.split(',') if l.strip()]
    entry.suggested_tactics = [t.strip() for t in entry.existing_tactics.split(',') if t.strip()]
    entry.confidence = 0.3


# ─── 提示词构建 ───

def build_prompt(entry: SorryEntry, module_description: str) -> str:
    return f"""你是一位 Lean 4 形式化数学专家。请为以下定理中的 sorry 提供详细的证明策略分析。

## 定理信息

- **定理名称**: {entry.theorem_name}
- **类型**: {entry.theorem_type}
- **文件**: {entry.file_path}
- **行号**: {entry.line_number}
- **模块描述**: {module_description}

## 已有策略注释

- **PFE ENGINEERING NOTE**: {entry.engineering_note or "无"}
- **STRATEGY**: {entry.existing_strategy or "无"}
- **LEMMAS NEEDED**: {entry.existing_lemmas or "无"}
- **TACTICS NEEDED**: {entry.existing_tactics or "无"}

## 定理声明

```lean
{entry.statement}
```

## 请提供以下分析（用中文）

1. **证明策略概述**: 该定理的数学背景、证明思路
2. **每个 sorry 的详细步骤**: 如何分解问题、使用什么数学工具
3. **建议引理 (suggested_lemmas)**: 列出 3-8 个可能的 Mathlib 引理名称
4. **建议策略 (suggested_tactics)**: 列出 3-8 个推荐的 Lean 4 tactics
5. **难度评估 (difficulty)**: 1-10 的整数
6. **置信度 (confidence)**: 0.0-1.0 的浮点数，表示你对策略的信心

请以如下结构化格式输出：

```
STRATEGY: <详细策略>
DIFFICULTY: <1-10>
CONFIDENCE: <0.0-1.0>
LEMMAS: <引理1>, <引理2>, ...
TACTICS: <tactic1>, <tactic2>, ...
```"""


def parse_llm_response(response: str) -> Dict[str, Any]:
    """从 LLM 响应中提取结构化字段。"""
    result = {
        "strategy": response,
        "difficulty": 5,
        "confidence": 0.5,
        "lemmas": [],
        "tactics": [],
    }

    # 提取 DIFFICULTY
    dm = re.search(r'DIFFICULTY[:\s]+(\d+)', response, re.IGNORECASE)
    if dm:
        result["difficulty"] = min(10, max(1, int(dm.group(1))))

    # 提取 CONFIDENCE
    cm = re.search(r'CONFIDENCE[:\s]+([0-9.]+)', response, re.IGNORECASE)
    if cm:
        result["confidence"] = min(1.0, max(0.0, float(cm.group(1))))

    # 提取 LEMMAS
    lm = re.search(r'LEMMAS?[:\s]+(.+?)(?:\n|TACTICS|CONFIDENCE|DIFFICULTY|$)', response, re.IGNORECASE | re.DOTALL)
    if lm:
        lemma_text = lm.group(1)
        result["lemmas"] = [l.strip() for l in re.split(r'[,;]', lemma_text) if l.strip()]

    # 提取 TACTICS
    tm = re.search(r'TACTICS?[:\s]+(.+?)(?:\n|LEMMAS|CONFIDENCE|DIFFICULTY|$)', response, re.IGNORECASE | re.DOTALL)
    if tm:
        tactic_text = tm.group(1)
        result["tactics"] = [t.strip() for t in re.split(r'[,;]', tactic_text) if t.strip()]

    # 提取 STRATEGY
    sm = re.search(r'STRATEGY[:\s]+(.+?)(?:\nDIFFICULTY|\nCONFIDENCE|\nLEMMAS|\nTACTICS|$)', response, re.IGNORECASE | re.DOTALL)
    if sm:
        result["strategy"] = sm.group(1).strip()

    return result


# ─── 报告生成 ───

def generate_markdown_report(report: SorryReport) -> str:
    lines = [
        "# TOE-SYLVA Sorry 策略生成报告",
        "",
        f"**生成时间**: {report.generated_at}",
        f"**扫描文件数**: {report.total_files}",
        f"**扫描定理数**: {report.total_theorems}",
        f"**Total sorry**: {report.total_sorry}",
        f"**API 错误数**: {len(report.api_errors)}",
        "",
        "---",
        "",
    ]

    for i, entry in enumerate(report.entries, 1):
        lines.extend([
            f"## {i}. `{entry.theorem_name}` ({entry.theorem_type})",
            "",
            f"- **文件**: `{entry.file_path}`",
            f"- **行号**: {entry.line_number}",
            f"- **难度**: {entry.difficulty}/10",
            f"- **置信度**: {entry.confidence:.2f}",
            f"- **LLM 延迟**: {entry.llm_latency_ms}ms",
            "",
            "### 定理声明",
            "",
            "```lean",
            entry.statement,
            "```",
            "",
        ])

        if entry.existing_strategy or entry.engineering_note:
            lines.extend([
                "### 已有注释",
                "",
            ])
            if entry.existing_strategy:
                lines.append(f"- **STRATEGY**: {entry.existing_strategy}")
            if entry.existing_lemmas:
                lines.append(f"- **LEMMAS NEEDED**: {entry.existing_lemmas}")
            if entry.existing_tactics:
                lines.append(f"- **TACTICS NEEDED**: {entry.existing_tactics}")
            if entry.engineering_note:
                lines.append(f"- **ENGINEERING NOTE**: {entry.engineering_note}")
            lines.append("")

        lines.extend([
            "### LLM 生成策略",
            "",
            entry.strategy,
            "",
            "### 建议引理",
            "",
        ])
        for lemma in entry.suggested_lemmas:
            lines.append(f"- `{lemma}`")
        lines.extend([
            "",
            "### 建议 Tactics",
            "",
        ])
        for tactic in entry.suggested_tactics:
            lines.append(f"- `{tactic}`")
        lines.extend([
            "",
            "---",
            "",
        ])

    if report.api_errors:
        lines.extend([
            "# API 错误日志",
            "",
        ])
        for err in report.api_errors:
            lines.append(f"- {err}")
        lines.append("")

    return "\n".join(lines)


# ─── 主流程 ───

def main():
    parser = argparse.ArgumentParser(description='Generate sorry strategies for TOE-SYLVA via Zhipu GLM-5.1')
    parser.add_argument('--sylva-dir', default=TOE_SYLVA_DEFAULT, help='TOE-SYLVA directory')
    parser.add_argument('--output-dir', default='reports', help='Output directory for report')
    parser.add_argument('--max-sorry', type=int, default=0, help='Max sorry to analyze (0=all)')
    parser.add_argument('--dry-run', action='store_true', help='Skip API calls, use fallback only')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    sylva_dir = Path(args.sylva_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not sylva_dir.exists():
        print(f"[ERROR] TOE-SYLVA directory not found: {sylva_dir}")
        sys.exit(1)

    # 检查 API Key
    api_key = get_zhipu_api_key()
    if not api_key:
        print("[WARNING] No ZHIPU_API_KEY found. Will use fallback strategies only.")
    else:
        print(f"[INFO] Zhipu API key found (len={len(api_key)})")

    # 1. 解析 Lean 文件
    print(f"[Phase 1] Parsing Lean files from {sylva_dir}...")
    lean_parser = LeanParser(sylva_dir)
    lean_parser.parse_all()
    print(f"  -> Parsed {len(lean_parser.modules)} modules")

    # 2. 收集所有 sorry
    print("[Phase 2] Collecting sorry entries...")
    entries: List[SorryEntry] = []
    for module in lean_parser.modules:
        for decl in module['theorems'] + module['definitions'] + module['axioms']:
            if not decl['has_sorry']:
                continue
            for sorry_line in decl['sorry_lines']:
                entry = SorryEntry(
                    theorem_name=decl['name'],
                    file_path=module['file_path'],
                    line_number=sorry_line,
                    theorem_type=decl['type'],
                    statement=decl['statement'],
                    existing_strategy=decl.get('strategy', ''),
                    existing_lemmas=decl.get('lemmas_needed', ''),
                    existing_tactics=decl.get('tactics_needed', ''),
                    engineering_note=decl.get('engineering_note', ''),
                )
                entries.append(entry)

    total_theorems = sum(
        len(m['theorems']) + len(m['definitions']) + len(m['axioms'])
        for m in lean_parser.modules
    )
    print(f"  -> Found {len(entries)} sorry entries in {total_theorems} declarations")

    # 限制数量
    if args.max_sorry > 0 and len(entries) > args.max_sorry:
        print(f"  -> Limiting to {args.max_sorry} entries (as requested)")
        entries = entries[:args.max_sorry]

    # 3. 调用 LLM 分析每个 sorry
    print("[Phase 3] Generating strategies via Zhipu GLM-5.1...")
    api_errors = []
    for i, entry in enumerate(entries, 1):
        print(f"  [{i}/{len(entries)}] {entry.theorem_name} (line {entry.line_number})...", end=" ")

        if args.dry_run or not api_key:
            fallback_strategy(entry)
            print("[FALLBACK]")
            continue

        module_desc = next(
            (m['description'] for m in lean_parser.modules if m['file_path'] == entry.file_path),
            ""
        )
        prompt = build_prompt(entry, module_desc)
        system = "You are a formal mathematics expert specializing in Lean 4 proof assistant. Analyze incomplete proofs and provide detailed strategies for completing them. Respond in Chinese."

        result = call_zhipu_glm51(prompt, system)
        if result.get("error"):
            api_errors.append(f"{entry.theorem_name}: {result['error']}")
            fallback_strategy(entry)
            print(f"[FALLBACK] ({result['error'][:50]})")
        else:
            parsed = parse_llm_response(result["content"])
            entry.strategy = parsed["strategy"]
            entry.difficulty = parsed["difficulty"]
            entry.confidence = parsed["confidence"]
            entry.suggested_lemmas = parsed["lemmas"]
            entry.suggested_tactics = parsed["tactics"]
            entry.llm_response = result["content"]
            entry.llm_latency_ms = result["latency_ms"]
            print(f"[OK] difficulty={entry.difficulty}, confidence={entry.confidence:.2f}, latency={entry.llm_latency_ms}ms")

        # 简单速率限制
        time.sleep(0.5)

    # 4. 生成报告
    print("[Phase 4] Generating Markdown report...")
    report = SorryReport(
        generated_at=datetime.now().isoformat(),
        total_files=len(lean_parser.modules),
        total_theorems=total_theorems,
        total_sorry=len(entries),
        entries=entries,
        api_errors=api_errors,
    )

    md_content = generate_markdown_report(report)
    report_path = output_dir / f"sorry_strategies_{datetime.now().strftime('%Y%m%d')}.md"
    report_path.write_text(md_content, encoding='utf-8')
    print(f"  -> Markdown report: {report_path}")

    # 同时保存 JSON
    json_path = output_dir / f"sorry_strategies_{datetime.now().strftime('%Y%m%d')}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            "generated_at": report.generated_at,
            "total_files": report.total_files,
            "total_theorems": report.total_theorems,
            "total_sorry": report.total_sorry,
            "api_errors": report.api_errors,
            "entries": [e.to_dict() for e in report.entries],
        }, f, ensure_ascii=False, indent=2)
    print(f"  -> JSON data: {json_path}")

    print(f"\n[Done] Analyzed {len(entries)} sorry entries. {len(api_errors)} API errors.")
    if report_path.exists():
        print(f"Report saved to: {report_path.absolute()}")


if __name__ == '__main__':
    main()
