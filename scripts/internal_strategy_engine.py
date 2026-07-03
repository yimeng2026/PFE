#!/usr/bin/env python3
"""
Internal Strategy Engine — "自己的 API"
基于数学知识库 + 规则模板生成 Lean 4 证明策略
不依赖外部 LLM API（Zhipu/Kimi/OpenAI），零成本、零延迟、可审计

使用方法：
    python internal_strategy_engine.py --file <lean_file> --output <output_dir>
    python internal_strategy_engine.py --analyze-all --project <project_dir>

作者：PFE 工程团队
版本：v1.0
日期：2026-07-03
"""

import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class StrategyResult:
    """单个 sorry 的策略分析结果"""
    theorem_name: str
    file_path: str
    line_number: int
    context: str
    sorry_type: str  # numerical, algebraic, set, inequality, existence, universal, induction, millennium, etc.
    confidence: float  # 0-1
    strategy_chain: List[str]
    comment_block: str
    lemmas_needed: List[str]
    tactics_needed: List[str]
    numerical_verification: str
    references: List[str]


class InternalStrategyEngine:
    """
    内置策略引擎 — "自己的 API"
    基于规则 + 模板 + 知识库生成 Lean 4 证明策略
    """

    # ───────────────────────────────────────────
    # 知识库：策略类型 → 自动证明策略列表
    # ───────────────────────────────────────────
    KNOWLEDGE_BASE = {
        "numerical": [
            "norm_num",
            "omega",
            "native_decide",
            "decide",
            "simp; norm_num",
        ],
        "algebraic_identity": [
            "ring",
            "ring_nf",
            "field_simp",
            "norm_num",
            "simp; ring",
        ],
        "inequality": [
            "linarith",
            "nlinarith",
            "positivity",
            "by_contra; push_neg",
            "apply le_trans",
            "apply lt_trans",
        ],
        "set_membership": [
            "intro",
            "simp",
            "exact",
            "refine",
            "constructor",
            "use",
        ],
        "existence": [
            "use",
            "refine",
            "constructor",
            "rcases",
            "obtain",
            "have",
        ],
        "universal": [
            "intro",
            "apply",
            "specialize",
            "have",
        ],
        "induction": [
            "induction",
            "cases",
            "fin_cases",
            "rcases",
            "refine",
        ],
        "contradiction": [
            "by_contra",
            "push_neg",
            "contradiction",
            "exfalso",
            "apply not_not.mp",
        ],
        "finrank": [
            "rw [LinearEquiv.finrank_eq]",
            "rw [Module.finrank_tensorProduct]",
            "rw [DirectSum.finrank_sum]",
            "simp [hodgeNumber]",
            "ring",
        ],
        "gamma_function": [
            "apply Complex.Gamma_ne_zero_of_re_pos",
            "apply Real.Gamma_pos",
            "positivity",
            "nlinarith",
        ],
        "energy_estimate": [
            "nlinarith",
            "apply Gronwall.le_of_gronwall",
            "apply Sobolev.embedding",
            "norm_num",
        ],
        "millennium_prize": [
            "PFE ENGINEERING NOTE",
            "Numerical verification: MPMath/Arb",
            "Reference: Clay Mathematics Institute",
        ],
    }

    # ───────────────────────────────────────────
    # 模板库：按数学领域分类的注释模板
    # ───────────────────────────────────────────
    TEMPLATE_LIBRARY = {
        "hodge_theory": {
            "problem": "Hodge structure {V, hodge decomposition, Hodge numbers} satisfies Betti number = sum of Hodge numbers.",
            "strategy": "Use LinearEquiv.finrank_eq for isomorphism, Module.finrank_tensorProduct for tensor products, DirectSum.finrank_sum for direct sums.",
            "lemmas": ["LinearEquiv.finrank_eq", "Module.finrank_tensorProduct", "DirectSum.finrank_sum", "hodgeNumber"],
            "tactics": ["rw", "simp", "ring", "constructor"],
            "confidence": 0.90,
            "references": ["Griffiths & Harris, Principles of Algebraic Geometry, Chap. 0"],
        },
        "riemann_hypothesis": {
            "problem": "BootstrapResidual minimization at sigma=1/2 implies Riemann Hypothesis.",
            "strategy": "Convex analysis + symmetry of Xi function. Show sigma_star = 1/2 is the unique minimizer.",
            "lemmas": ["BootstrapResidual_convex", "XiSquaredMag_symmetry", "ConvexOn.unique_minimizer"],
            "tactics": ["nlinarith", "by_contra", "apply ConvexOn.unique_minimizer"],
            "confidence": 0.15,
            "references": ["Odlyzko 2003", "Gourdon 2004", "Platt 2011", "Titchmarsh, Theory of the Riemann Zeta Function"],
        },
        "navier_stokes": {
            "problem": "Energy estimate / blow-up criterion / regularity for Navier-Stokes equations.",
            "strategy": "Energy method + Sobolev embedding + Gronwall inequality. Use sylva_ns_regularity axiom for small data.",
            "lemmas": ["sylva_ns_regularity", "energy_inequality", "Sobolev.embedding", "Gronwall.le_of_gronwall"],
            "tactics": ["nlinarith", "apply", "have", "linarith"],
            "confidence": 0.25,
            "references": ["Temam, Navier-Stokes Equations", "Leray 1934", "Beale-Kato-Majda 1984"],
        },
        "complexity": {
            "problem": "P vs NP related: entropy gap, Cook-Levin theorem, Shannon counting.",
            "strategy": "Constructive separation + cardinality arguments + entropy bounds. Use SAT as witness.",
            "lemmas": ["SAT_in_NP", "CookLevin_theorem", "shannon_counting_argument", "entropy_gap_monotonicity"],
            "tactics": ["by_contra", "use", "rcases", "norm_num", "omega"],
            "confidence": 0.05,
            "references": ["Cook 1971", "Levin 1973", "Shannon 1948", "Arora & Barak, Computational Complexity"],
        },
        "numerical_verification": {
            "problem": "Numerical verification of Riemann zeta zeros on critical line.",
            "strategy": "Riemann-Siegel formula + Odlyzko's algorithm. Verify |zeta(1/2 + i*gamma)| < epsilon.",
            "lemmas": ["riemannZeta_def", "RiemannSiegel_formula", "critical_line_property"],
            "tactics": ["native_decide", "norm_num", "simp", "unfold"],
            "confidence": 0.02,
            "references": ["Odlyzko 1987", "Gourdon 2004", "Titchmarsh §4.17", "Edwards §6.5"],
        },
        "superconductivity": {
            "problem": "Pairing symmetry classification or material derivation from theory.",
            "strategy": "Representation theory + group theory. Use finite group enumeration for simple cases.",
            "lemmas": ["representation_theory", "group_characters", "Wyckoff_positions"],
            "tactics": ["decide", "omega", "fin_cases", "simp"],
            "confidence": 0.40,
            "references": ["Bardeen-Cooper-Schrieffer 1957", "Anderson 1987"],
        },
        "emergent_math": {
            "problem": "Emergent mathematical structure from physical constraints.",
            "strategy": "Show structure satisfies axioms via construction. Use phi properties for self-similar cases.",
            "lemmas": ["phi_pos", "phi_sq_eq_phi_add_one", "self_similarity"],
            "tactics": ["use", "constructor", "rfl", "nlinarith"],
            "confidence": 0.85,
            "references": ["SYLVA Emergent Mathematics Framework", "Golden Ratio in Physics"],
        },
    }

    # ───────────────────────────────────────────
    # 自动分类规则：基于上下文关键词匹配
    # ───────────────────────────────────────────
    CLASSIFICATION_RULES = [
        (r"\bfinrank\b|\bHodge\b|\bBetti\b|\bhodgeNumber\b", "hodge_theory", "finrank"),
        (r"\briemannZeta\b|\bBootstrapResidual\b|\bsigma_star\b|\bXi\b", "riemann_hypothesis", "millennium_prize"),
        (r"\bNavierStokes\b|\benergy\b|\bSobolev\b|\bGronwall\b|\bblow.up\b", "navier_stokes", "energy_estimate"),
        (r"\bClassP\b|\bClassNP\b|\bSAT\b|\bentropy_gap\b|\bCookLevin\b", "complexity", "millennium_prize"),
        (r"\briemannZeta\b.*\bgamma\b|\bzetaHardyZ\b|\bgramPoint\b", "numerical_verification", "millennium_prize"),
        (r"\bPairingSymmetry\b|\bWyckoffPosition\b|\bmaterial_family\b", "superconductivity", "set_membership"),
        (r"\bEmergentStructure\b|\bGoldenRatio\b|\bphi\b|\bself_similar\b", "emergent_math", "algebraic_identity"),
        (r"\bmodMul\b|\bcoreFactor\b|\bdetectsFactor\b", "number_theory", "numerical"),
        (r"\bGF3\b|\bGF9\b|\bFrobenius\b|\bfield\b", "finite_field", "algebraic_identity"),
    ]

    def __init__(self):
        self.results: List[StrategyResult] = []

    def classify_sorry(self, context: str, theorem_name: str) -> Tuple[str, str]:
        """
        基于上下文自动分类 sorry 类型
        返回: (domain, strategy_type)
        """
        context_lower = context.lower()
        name_lower = theorem_name.lower()

        for pattern, domain, strategy_type in self.CLASSIFICATION_RULES:
            if re.search(pattern, context, re.IGNORECASE) or re.search(pattern, theorem_name, re.IGNORECASE):
                return domain, strategy_type

        # 默认分类
        if any(kw in context_lower for kw in ["0 <", "> 0", "= 0", "≤", "≥", "<", ">"]):
            return "general", "inequality"
        if any(kw in context_lower for kw in ["∀", "forall", "∀"]):
            return "general", "universal"
        if any(kw in context_lower for kw in ["∃", "exists", "∃"]):
            return "general", "existence"
        if any(kw in context_lower for kw in ["∈", "set", "subset"]):
            return "general", "set_membership"
        if any(kw in context_lower for kw in ["+", "-", "*", "/", "^", "ring"]):
            return "general", "algebraic_identity"

        return "general", "numerical"

    def generate_strategy_chain(self, domain: str, strategy_type: str) -> List[str]:
        """生成策略链（5 层 try 块）"""
        base_strategies = self.KNOWLEDGE_BASE.get(strategy_type, ["simp", "norm_num", "omega"])

        # 根据领域添加专用策略
        domain_strategies = []
        if domain in self.TEMPLATE_LIBRARY:
            domain_strategies = self.TEMPLATE_LIBRARY[domain].get("tactics", [])

        # 组合：领域专用 + 基础策略
        chain = domain_strategies[:2]  # 前两个用领域专用
        chain.extend(base_strategies[:3])  # 后三个用基础策略

        return chain[:5]  # 最多 5 层

    def generate_comment_block(self, theorem_name: str, domain: str, strategy_type: str,
                               confidence: float, context: str) -> str:
        """生成千界花园八要素注释块"""
        template = self.TEMPLATE_LIBRARY.get(domain, {
            "problem": f"Proof of {theorem_name}.",
            "strategy": "Apply standard tactics and simplify.",
            "lemmas": ["Mathlib standard lemmas"],
            "tactics": ["simp", "norm_num", "omega"],
            "confidence": confidence,
            "references": ["Mathlib documentation"],
        })

        # 根据 confidence 生成星级
        stars = "★" * int(confidence * 5) + "☆" * (5 - int(confidence * 5))

        block = f"""-- ╔══════════════════════════════════════════════════════════════════════╗
-- ║ 千界花园策略块 — {theorem_name}
-- ║ 问题：{template['problem']}
-- ║ 策略：{template['strategy']}
-- ║ 引理需求：{', '.join(template['lemmas'])}
-- ║ 策略需求：{', '.join(template['tactics'])}
-- ║ 置信度：{stars} ({confidence:.2f})
-- ║ 数值验证：{template.get('numerical_verification', 'N/A')}
-- ║ 已知结果：{', '.join(template['references'])}
-- ║ PFE PIPELINE：Add to {domain} verification targets
-- ╚══════════════════════════════════════════════════════════════════════╝"""
        return block

    def analyze_sorry(self, file_path: str, theorem_name: str, line_number: int,
                      context: str) -> StrategyResult:
        """分析单个 sorry，生成完整策略结果"""
        domain, strategy_type = self.classify_sorry(context, theorem_name)
        strategy_chain = self.generate_strategy_chain(domain, strategy_type)

        template = self.TEMPLATE_LIBRARY.get(domain, {})
        confidence = template.get("confidence", 0.5)

        # Millennium Prize 降低置信度
        if strategy_type == "millennium_prize":
            confidence = 0.05

        comment_block = self.generate_comment_block(
            theorem_name, domain, strategy_type, confidence, context
        )

        return StrategyResult(
            theorem_name=theorem_name,
            file_path=file_path,
            line_number=line_number,
            context=context[:200],  # 截断
            sorry_type=strategy_type,
            confidence=confidence,
            strategy_chain=strategy_chain,
            comment_block=comment_block,
            lemmas_needed=template.get("lemmas", ["Mathlib standard lemmas"]),
            tactics_needed=strategy_chain,
            numerical_verification=template.get("numerical_verification", "N/A"),
            references=template.get("references", ["Mathlib documentation"]),
        )

    def analyze_file(self, file_path: str) -> List[StrategyResult]:
        """分析单个 Lean 文件中的所有 sorry"""
        content = Path(file_path).read_text(encoding="utf-8")
        lines = content.split("\n")

        results = []
        current_theorem = None

        for i, line in enumerate(lines):
            # 检测 theorem/lemma 声明
            theorem_match = re.match(r"^(theorem|lemma|def)\s+(\w+)", line.strip())
            if theorem_match:
                current_theorem = theorem_match.group(2)

            # 检测 sorry
            if "sorry" in line and current_theorem:
                # 提取上下文（前20行到后5行）
                start = max(0, i - 20)
                end = min(len(lines), i + 5)
                context = "\n".join(lines[start:end])

                result = self.analyze_sorry(
                    file_path=file_path,
                    theorem_name=current_theorem,
                    line_number=i + 1,
                    context=context,
                )
                results.append(result)

        return results

    def generate_report(self, results: List[StrategyResult]) -> str:
        """生成 Markdown 报告"""
        report = f"""# 千界花园策略分析报告 — 自己的 API

> **生成时间：** 2026-07-03  
> **引擎版本：** InternalStrategyEngine v1.0  
> **总计 sorry：** {len(results)}  
> **平均置信度：** {sum(r.confidence for r in results) / max(len(results), 1):.2f}

---

## 分类统计

| 领域 | 数量 | 平均置信度 |
|------|------|-----------|
"""
        # 按领域统计
        domain_stats: Dict[str, List[float]] = {}
        for r in results:
            domain = r.file_path.split("/")[-1].replace(".lean", "")
            if domain not in domain_stats:
                domain_stats[domain] = []
            domain_stats[domain].append(r.confidence)

        for domain, confidences in sorted(domain_stats.items()):
            report += f"| {domain} | {len(confidences)} | {sum(confidences)/len(confidences):.2f} |\n"

        report += "\n---\n\n## 详细分析\n\n"

        for r in results:
            report += f"""### {r.theorem_name} ({r.file_path}:{r.line_number})

- **类型：** {r.sorry_type}
- **置信度：** {r.confidence:.2f}
- **策略链：** {r.strategy_chain}
- **引理需求：** {r.lemmas_needed}
- **数值验证：** {r.numerical_verification}
- **参考文献：** {r.references}

```lean
{r.comment_block}
```

---

"""
        return report

    def save_results(self, results: List[StrategyResult], output_dir: str):
        """保存结果到 JSON 和 Markdown 报告"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # JSON 结果
        json_path = output_path / "strategy_results.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([asdict(r) for r in results], f, ensure_ascii=False, indent=2)

        # Markdown 报告
        report_path = output_path / "strategy_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(self.generate_report(results))

        print(f"Results saved to {output_dir}")
        print(f"  - JSON: {json_path}")
        print(f"  - Report: {report_path}")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Internal Strategy Engine — 自己的 API")
    parser.add_argument("--file", help="Single Lean file to analyze")
    parser.add_argument("--project", help="Project directory to analyze all .lean files")
    parser.add_argument("--output", default="./reports", help="Output directory for results")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample data")

    args = parser.parse_args()

    engine = InternalStrategyEngine()

    if args.demo:
        # Demo mode: analyze a sample sorry
        result = engine.analyze_sorry(
            file_path="Hodge.lean",
            theorem_name="betti_number_eq_sum_hodge_numbers",
            line_number=540,
            context="""theorem betti_number_eq_sum_hodge_numbers {n : ℕ} (H : HodgeStructure n) :
    FiniteDimensional.finrank ℚ H.H_Q = ∑ p q : ℕ, hodgeNumber H p q := by
    rw [LinearEquiv.finrank_eq H.total_iso]
    -- need more steps...
    sorry""",
        )
        print("=== Demo Result ===")
        print(f"Theorem: {result.theorem_name}")
        print(f"Confidence: {result.confidence}")
        print(f"Strategy Chain: {result.strategy_chain}")
        print("\nComment Block:")
        print(result.comment_block)
        return

    if args.file:
        results = engine.analyze_file(args.file)
        engine.save_results(results, args.output)
        print(f"\nAnalyzed {len(results)} sorry(s) in {args.file}")
    elif args.project:
        all_results = []
        for lean_file in Path(args.project).rglob("*.lean"):
            if ".lake" in str(lean_file) or "archive" in str(lean_file):
                continue
            results = engine.analyze_file(str(lean_file))
            all_results.extend(results)
            print(f"  {lean_file}: {len(results)} sorry(s)")
        engine.save_results(all_results, args.output)
        print(f"\nTotal: {len(all_results)} sorry(s) analyzed")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
