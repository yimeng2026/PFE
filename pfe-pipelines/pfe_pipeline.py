#!/usr/bin/env python3
"""
PFE 自动化管道 — 端到端数值验证与工程拟合

质空论工程实践：从抽象拓扑（空）到物理可测量（质）的自动化涌现。

功能：
1. 读取 TOE-SYLVA 的 Lean 文件，提取数学定义
2. 转化为数值验证算法（SageMath/Python）
3. 执行计算并验证结果
4. 生成工程报告（置信度、误差范围、可复现性）
5. 通过 LLM 分析结果，为 TOE-SYLVA 提供启发

依赖：
- Python 3.8+
- numpy, scipy, matplotlib（数值计算和可视化）
- requests（调用千界花园 API）
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime


@dataclass
class VerificationResult:
    """数值验证结果 — 质空论工程涌现的标准输出格式"""
    module_name: str
    theorem_name: str
    status: str  # "PASS", "FAIL", "HEURISTIC", "ERROR"
    confidence: float  # 0.0-1.0
    numeric_value: Optional[float] = None
    expected_value: Optional[float] = None
    error_bound: Optional[float] = None
    computation_time_ms: Optional[int] = None
    notes: str = ""
    
    def to_dict(self):
        return asdict(self)


class LeanParser:
    """轻量 Lean 文本扫描器；结果不是 Lean 编译或证明状态。"""

    THEOREM_PATTERN = re.compile(
        r"^(theorem|lemma|def|axiom|conjecture|structure|inductive|instance)\s+"
        r"([a-zA-Z_][a-zA-Z0-9_']*)\b"
    )
    DECLARATION_START_PATTERN = re.compile(
        r"^(theorem|lemma|def|axiom|conjecture|structure|inductive|instance|example)\b"
    )
    SORRY_PATTERN = re.compile(r"\bsorry\b")
    STRING_LITERAL_PATTERN = re.compile(r'"(?:\\.|[^"\\])*"')
    IMPORT_PATTERN = re.compile(r"^import\s+(.+)")
    NAMESPACE_PATTERN = re.compile(r"^namespace\s+([a-zA-Z_][a-zA-Z0-9_]*)")

    def __init__(self, lean_dir: str):
        self.lean_dir = Path(lean_dir)
        self.modules: List[Dict] = []

    @classmethod
    def _strip_comments(cls, lines: List[str]) -> List[str]:
        """移除行注释和可嵌套块注释，同时保留字符串与原始行号。"""
        cleaned = []
        block_depth = 0
        in_string = False
        for line in lines:
            output = []
            i = 0
            while i < len(line):
                pair = line[i:i + 2]
                char = line[i]
                if block_depth:
                    if pair == "/-":
                        block_depth += 1
                        i += 2
                    elif pair == "-/":
                        block_depth -= 1
                        i += 2
                    else:
                        i += 1
                    continue
                if in_string:
                    output.append(char)
                    if char == "\\" and i + 1 < len(line):
                        output.append(line[i + 1])
                        i += 2
                        continue
                    if char == '"':
                        in_string = False
                    i += 1
                    continue
                if pair == "--":
                    break
                if pair == "/-":
                    block_depth = 1
                    i += 2
                    continue
                output.append(char)
                if char == '"':
                    in_string = True
                i += 1
            cleaned.append("".join(output))
        return cleaned

    @classmethod
    def _has_sorry(cls, line: str) -> bool:
        code = cls.STRING_LITERAL_PATTERN.sub('""', line)
        return cls.SORRY_PATTERN.search(code) is not None

    def parse_file(self, file_path: Path) -> Dict:
        """解析单个 Lean 文件；接受 Path 或路径字符串。"""
        file_path = Path(file_path)
        content = file_path.read_text(encoding="utf-8")
        raw_lines = content.split("\n")
        lines = self._strip_comments(raw_lines)

        module: Dict = {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "total_lines": len(raw_lines),
            "theorems": [],
            "definitions": [],
            "axioms": [],
            "sorry_count": 0,
            "sorry_lines": [],
            "imports": [],
            "namespace": "",
            "description": "",
            "analysis_mode": "text_only_not_compiled",
        }

        desc_lines = []
        for line in raw_lines[:30]:
            if line.strip().startswith("-") or line.strip().startswith("/"):
                desc_lines.append(line.strip().lstrip("-/").strip())
            elif line.strip() and not line.strip().startswith("import"):
                break
        module["description"] = " ".join(desc_lines)[:200]

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if m := self.IMPORT_PATTERN.match(stripped):
                module["imports"].append(m.group(1).strip())
            if m := self.NAMESPACE_PATTERN.match(stripped):
                module["namespace"] = m.group(1)

            if m := self.THEOREM_PATTERN.match(stripped):
                decl_type = m.group(1)
                decl_name = m.group(2)
                decl_sorry_lines = []
                for j in range(i, len(lines) + 1):
                    candidate = lines[j - 1].strip()
                    if j > i and self.DECLARATION_START_PATTERN.match(candidate):
                        break
                    if self._has_sorry(candidate):
                        decl_sorry_lines.append(j)

                decl = {
                    "name": decl_name,
                    "type": decl_type,
                    "line": i,
                    "has_sorry": bool(decl_sorry_lines),
                    "sorry_count": len(decl_sorry_lines),
                    "sorry_lines": decl_sorry_lines,
                    "statement": stripped[:200],
                }
                if decl_type in ("theorem", "lemma"):
                    module["theorems"].append(decl)
                elif decl_type == "def":
                    module["definitions"].append(decl)
                elif decl_type == "axiom":
                    module["axioms"].append(decl)

            if self._has_sorry(line):
                module["sorry_count"] += 1
                module["sorry_lines"].append(i)

        return module

    def parse_all(self) -> List[Dict]:
        """解析全部输入；缺失目录、空输入和读取错误均明确失败。"""
        if not self.lean_dir.is_dir():
            raise FileNotFoundError(f"Lean input directory not found: {self.lean_dir}")
        self.modules = []
        lean_files = sorted(self.lean_dir.rglob("*.lean"))
        for lean_file in lean_files:
            if ".lake" in lean_file.parts or "archive" in lean_file.parts:
                continue
            self.modules.append(self.parse_file(lean_file))
        if not self.modules:
            raise ValueError(f"No Lean files found outside .lake/archive: {self.lean_dir}")
        return self.modules
    
    def get_sorry_summary(self) -> Dict:
        """获取 sorry 分布摘要"""
        total_sorry = sum(m['sorry_count'] for m in self.modules)
        sorry_by_file = sorted(
            [(m['file_name'], m['sorry_count']) for m in self.modules if m['sorry_count'] > 0],
            key=lambda x: x[1], reverse=True
        )
        
        open_theorems = []
        for m in self.modules:
            for t in m['theorems']:
                if t['has_sorry']:
                    open_theorems.append({
                        'file': m['file_name'],
                        'theorem': t['name'],
                        'line': t['line'],
                        'sorry_count': t['sorry_count']
                    })
        
        return {
            'total_modules': len(self.modules),
            'total_sorry': total_sorry,
            'total_theorems': sum(len(m['theorems']) for m in self.modules),
            'total_axioms': sum(len(m['axioms']) for m in self.modules),
            'sorry_by_file': sorry_by_file[:10],
            'open_theorems': open_theorems
        }


class PFEEngineeringPipeline:
    """
    PFE 工程管道 — 质空论涌现的自动化执行器
    
    将 TOE-SYLVA 的数学定义转化为数值实验，
    执行计算并评估"有效涌现"质量。
    """
    
    def __init__(self, sylva_dir: str, output_dir: str = "pfe-output"):
        self.sylva_dir = Path(sylva_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.parser = LeanParser(sylva_dir)
        self.results: List[VerificationResult] = []
    
    def run_parsing(self) -> Dict:
        """第一阶段：解析 TOE-SYLVA 的 Lean 代码"""
        print("[PFE Pipeline] Phase 1: Parsing TOE-SYLVA Lean files...")
        self.parser.parse_all()
        summary = self.parser.get_sorry_summary()
        
        # 保存解析结果
        output_path = self.output_dir / "sylva_parsed_summary.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"  -> Parsed {summary['total_modules']} modules")
        print(f"  -> Total theorems: {summary['total_theorems']}")
        print(f"  -> Total sorry: {summary['total_sorry']}")
        print(f"  -> Total axioms: {summary['total_axioms']}")
        print(f"  -> Saved to {output_path}")
        
        return summary
    
    def run_numerical_verification(self, target_modules: List[str]) -> List[VerificationResult]:
        """第二阶段：数值验证（针对指定模块）"""
        print(f"[PFE Pipeline] Phase 2: Numerical verification for {target_modules}...")
        
        for module_name in target_modules:
            # 查找对应的 Python 验证脚本
            py_script = self.sylva_dir.parent / "sagemath_verification" / f"{module_name.lower()}_verification.py"
            
            if py_script.exists():
                print(f"  -> Running {py_script.name}...")
                try:
                    # 这里可以调用 SageMath 或 Python 执行验证
                    result = subprocess.run(
                        [sys.executable, str(py_script)],
                        capture_output=True, text=True, timeout=300
                    )
                    
                    status = "PASS" if result.returncode == 0 else "FAIL"
                    self.results.append(VerificationResult(
                        module_name=module_name,
                        theorem_name="numerical_verification",
                        status=status,
                        confidence=0.95 if status == "PASS" else 0.5,
                        notes=result.stdout[:500] if result.stdout else "No output"
                    ))
                except Exception as e:
                    self.results.append(VerificationResult(
                        module_name=module_name,
                        theorem_name="numerical_verification",
                        status="ERROR",
                        confidence=0.0,
                        notes=str(e)
                    ))
            else:
                print(f"  -> No Python script found for {module_name}")
                self.results.append(VerificationResult(
                    module_name=module_name,
                    theorem_name="numerical_verification",
                    status="HEURISTIC",
                    confidence=0.3,
                    notes="No numerical verification script available; requires manual engineering"
                ))
        
        return self.results
    
    def run_llm_analysis(self, api_endpoint: Optional[str] = None) -> Dict:
        """第三阶段：LLM 分析（调用千界花园后端）"""
        print("[PFE Pipeline] Phase 3: LLM analysis of open problems...")
        
        # 构建提示
        open_theorems = []
        for m in self.parser.modules:
            for t in m['theorems']:
                if t['has_sorry']:
                    open_theorems.append(f"- {m['file_name']}::{t['name']} (line {t['line']}, {t['sorry_count']} sorry)")
        
        prompt = f"""作为 PFE 工程代理，分析以下 TOE-SYLVA 的开放问题，
为每个问题提供数值验证策略或工程近似方案。

开放问题列表：
{chr(10).join(open_theorems[:20])}

请为每个问题提供：
1. 数值验证方法（如果有）
2. 工程近似策略（如果数值验证不可行）
3. 置信度评估（0-1）
4. 所需的计算工具（SageMath/Python/Mathematica）

注意：PFE 追求有效涌现，不要求数学严格性。"""
        
        # 如果配置了千界花园 API，则调用
        if api_endpoint:
            try:
                import requests
                response = requests.post(
                    api_endpoint,
                    json={"prompt": prompt, "model": "glm-5.1"},
                    timeout=60
                )
                analysis = response.json()
                print(f"  -> LLM analysis received ({len(analysis.get('content', ''))} chars)")
                return {"status": "success", "analysis": analysis}
            except Exception as e:
                print(f"  -> LLM analysis failed: {e}")
                return {"status": "error", "error": str(e)}
        else:
            print("  -> No API endpoint configured; saving prompt for manual analysis")
            prompt_path = self.output_dir / "llm_analysis_prompt.txt"
            prompt_path.write_text(prompt, encoding='utf-8')
            return {"status": "pending", "prompt_file": str(prompt_path)}
    
    def generate_report(self) -> Path:
        """第四阶段：生成工程报告"""
        print("[PFE Pipeline] Phase 4: Generating engineering report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'pipeline': 'PFE Precision Fitting Engineering',
            'philosophy': 'Effective Emergence from Void to Mass (ZhiKong)',
            'sylva_summary': self.parser.get_sorry_summary(),
            'verification_results': [r.to_dict() for r in self.results],
            'quality_metrics': {
                'total_pass': sum(1 for r in self.results if r.status == 'PASS'),
                'total_fail': sum(1 for r in self.results if r.status == 'FAIL'),
                'total_heuristic': sum(1 for r in self.results if r.status == 'HEURISTIC'),
                'average_confidence': sum(r.confidence for r in self.results) / len(self.results) if self.results else 0
            }
        }
        
        report_path = self.output_dir / f"pfe_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"  -> Report saved to {report_path}")
        return report_path
    
    def run_full_pipeline(self, target_modules: Optional[List[str]] = None, llm_api: Optional[str] = None):
        """执行完整管道"""
        print("=" * 60)
        print("PFE Precision Fitting Engineering Pipeline")
        print("ZhiKong Prototype: Void -> Mass Effective Emergence")
        print("=" * 60)
        
        # Phase 1: Parse
        summary = self.run_parsing()
        
        # Phase 2: Numerical verification
        if target_modules:
            self.run_numerical_verification(target_modules)
        
        # Phase 3: LLM analysis
        self.run_llm_analysis(llm_api)
        
        # Phase 4: Report
        report_path = self.generate_report()
        
        print("=" * 60)
        print(f"Pipeline complete. Report: {report_path}")
        print("=" * 60)
        
        return report_path


def main():
    """CLI 入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PFE Engineering Pipeline')
    parser.add_argument('--sylva-dir', default='sylva-release/src', help='TOE-SYLVA Lean code directory')
    parser.add_argument('--output-dir', default='pfe-output', help='Output directory')
    parser.add_argument('--modules', nargs='+', help='Target modules for numerical verification')
    parser.add_argument('--llm-api', help='LLM API endpoint (e.g., http://localhost:3000/api/research/llm)')
    parser.add_argument('--parse-only', action='store_true', help='Only parse Lean files, skip verification')
    
    args = parser.parse_args()
    
    pipeline = PFEEngineeringPipeline(args.sylva_dir, args.output_dir)
    
    if args.parse_only:
        pipeline.run_parsing()
    else:
        pipeline.run_full_pipeline(args.modules, args.llm_api)


if __name__ == '__main__':
    main()
