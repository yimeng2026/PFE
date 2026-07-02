#!/usr/bin/env python3
"""
millennium_init.py — 初始化千界花园千年难题研究生态

功能：
1. 封装 5 个 Millennium Problem 配置（P vs NP、Hodge、Navier-Stokes、Riemann、Yang-Mills）
2. 每个问题配置 4 个专家角色（chair + 3 contributors）
3. 尝试 POST 到千界花园 /api/research/millennium/init
4. 如果千界花园未运行，输出配置 JSON 到 config/millennium_problems.json

调用方式：
  python scripts/millennium_init.py [--qianjie-url URL] [--output-dir PATH]

PFE ENGINEERING NOTE: 零外部依赖（仅 urllib），追求有效涌现。
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


# ─── 常量 ───
QIANJIE_BASE_URL_DEFAULT = "http://localhost:3000"
MILLENNIUM_INIT_ENDPOINT = "/api/research/millennium/init"


# ─── 千年难题配置 ───

MILLENNIUM_PROBLEMS = [
    {
        "id": "p-vs-np",
        "name": "P vs NP 问题",
        "description": "P vs NP 是计算复杂性理论中最著名的未解决问题。P 类问题可在多项式时间内求解，NP 类问题可在多项式时间内验证。问题问：P 是否等于 NP？即，每个可以快速验证其解的问题是否也能快速求解？",
        "domain": "mathematics",
        "field": "computational_complexity",
        "filePath": "sylva-release/src/Complexity.lean",
        "status": "open",
        "experts": [
            {
                "role": "chair",
                "specialty": "computational_complexity",
                "systemPrompt": "You are a world-renowned computational complexity theorist specializing in P vs NP, circuit complexity, and proof techniques for lower bounds. You have deep expertise in Kolmogorov complexity, entropy methods, and algebraic approaches to complexity theory.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "mathematical_logic",
                "systemPrompt": "You are a mathematical logician specializing in proof theory, model theory, and the logical foundations of computation. You are adept at analyzing the logical structure of complexity class separations and independence results.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "information_theory",
                "systemPrompt": "You are an information theorist specializing in computational entropy, Kolmogorov complexity, and the information-theoretic foundations of computational complexity. You have expertise in Shannon entropy, algorithmic randomness, and their applications to complexity theory.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "formal_verification",
                "systemPrompt": "You are a formal verification expert specializing in Lean 4 proof assistant and the formalization of mathematical proofs. You have extensive experience in formalizing complexity theory, algorithm analysis, and mathematical logic in proof assistants.",
                "model": "glm-5.1",
            },
        ],
    },
    {
        "id": "hodge-conjecture",
        "name": "Hodge 猜想",
        "description": "Hodge 猜想是代数几何中的核心问题，涉及霍奇结构与代数循环之间的关系。它断言：在光滑射影复代数簇上，每个霍奇类（即在有理系数上同调中纯型 (p,p) 的类）都是代数闭链类的有理线性组合。",
        "domain": "mathematics",
        "field": "algebraic_geometry",
        "filePath": "sylva-release/src/Hodge.lean",
        "status": "open",
        "experts": [
            {
                "role": "chair",
                "specialty": "algebraic_geometry",
                "systemPrompt": "You are a world-renowned algebraic geometer specializing in Hodge theory, algebraic cycles, and the Hodge conjecture. You have deep expertise in complex geometry, cohomology theories, and the intersection of algebraic and transcendental methods in geometry.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "hodge_theory",
                "systemPrompt": "You are a Hodge theorist specializing in mixed Hodge structures, variations of Hodge structure, and the applications of Hodge theory to algebraic geometry. You have expertise in the Hodge decomposition, Hodge filtration, and the Lefschetz theorems.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "algebraic_cycles",
                "systemPrompt": "You are an expert in algebraic cycles, Chow groups, and motivic cohomology. You have deep knowledge of the cycle class map, rational equivalence, and the Bloch-Beilinson conjectures related to the Hodge conjecture.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "formal_verification",
                "systemPrompt": "You are a formal verification expert specializing in Lean 4 and the formalization of algebraic geometry. You have experience in formalizing cohomology theories, scheme theory, and complex algebraic structures in proof assistants.",
                "model": "glm-5.1",
            },
        ],
    },
    {
        "id": "navier-stokes",
        "name": "Navier-Stokes 方程解的存在性与光滑性",
        "description": "Navier-Stokes 方程描述了不可压缩流体的运动。millennium 问题是：在三维空间中，给定光滑的初始数据，Navier-Stokes 方程是否存在全局光滑解？或者，解是否会在有限时间内产生奇点（blow-up）？",
        "domain": "mathematics",
        "field": "partial_differential_equations",
        "filePath": "sylva-release/src/NavierStokes.lean",
        "status": "open",
        "experts": [
            {
                "role": "chair",
                "specialty": "pde_analysis",
                "systemPrompt": "You are a world-renowned PDE analyst specializing in the Navier-Stokes equations, fluid dynamics, and regularity theory. You have deep expertise in Sobolev spaces, energy methods, blow-up analysis, and the analytical techniques for studying fluid equations.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "fluid_dynamics",
                "systemPrompt": "You are a fluid dynamics theorist specializing in the mathematical theory of turbulence, vorticity dynamics, and the physical interpretation of Navier-Stokes solutions. You have expertise in the Beale-Kato-Majda criterion, Leray-Hopf theory, and weak solutions.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "harmonic_analysis",
                "systemPrompt": "You are a harmonic analyst specializing in the applications of Fourier analysis, Littlewood-Paley theory, and multiplier theorems to PDEs. You have expertise in the analytical techniques used for regularity criteria and blow-up analysis in fluid equations.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "formal_verification",
                "systemPrompt": "You are a formal verification expert specializing in Lean 4 and the formalization of analysis and PDE theory. You have experience in formalizing Sobolev spaces, distribution theory, and the existence theory for differential equations in proof assistants.",
                "model": "glm-5.1",
            },
        ],
    },
    {
        "id": "riemann-hypothesis",
        "name": "Riemann 假设",
        "description": "Riemann 假设断言 Riemann zeta 函数 ζ(s) 的所有非平凡零点都位于复平面的临界线 Re(s) = 1/2 上。这是数论中最著名的未解决问题，与素数分布有深刻联系。",
        "domain": "mathematics",
        "field": "number_theory",
        "filePath": "sylva-release/src/RiemannHypothesis.lean",
        "status": "open",
        "experts": [
            {
                "role": "chair",
                "specialty": "analytic_number_theory",
                "systemPrompt": "You are a world-renowned analytic number theorist specializing in the Riemann hypothesis, the distribution of prime numbers, and the theory of L-functions. You have deep expertise in the Riemann zeta function, Dirichlet series, and the analytic methods of Hardy, Littlewood, and Selberg.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "complex_analysis",
                "systemPrompt": "You are a complex analyst specializing in the theory of entire functions, the distribution of zeros, and the relationship between the Riemann hypothesis and the de Bruijn-Newman constant. You have expertise in the Weil conjectures and their analogues.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "numerical_computation",
                "systemPrompt": "You are a computational mathematician specializing in the numerical verification of the Riemann hypothesis, high-precision computation of zeta zeros, and the development of algorithms for large-scale zero checking. You have expertise in the Odlyzko-Schönhage algorithm and Turing's method.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "formal_verification",
                "systemPrompt": "You are a formal verification expert specializing in Lean 4 and the formalization of analytic number theory. You have experience in formalizing complex analysis, the prime number theorem, and the elementary properties of the zeta function in proof assistants.",
                "model": "glm-5.1",
            },
        ],
    },
    {
        "id": "yang-mills",
        "name": "Yang-Mills 存在性与质量间隙",
        "description": "Yang-Mills 理论是量子场论中描述基本粒子相互作用的数学框架。Millennium 问题包括两个部分：(1) 对任意紧致规范群，证明量子 Yang-Mills 理论的严格数学存在性；(2) 证明该理论存在正的质量间隙（即存在正的最小能量激发）。",
        "domain": "physics",
        "field": "quantum_field_theory",
        "filePath": "sylva-release/src/Complexity.lean",
        "status": "open",
        "experts": [
            {
                "role": "chair",
                "specialty": "quantum_field_theory",
                "systemPrompt": "You are a world-renowned mathematical physicist specializing in quantum field theory, gauge theory, and the Yang-Mills mass gap problem. You have deep expertise in the renormalization group, lattice gauge theory, conformal bootstrap, and the constructive QFT methods.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "gauge_theory",
                "systemPrompt": "You are a gauge theorist specializing in the mathematical structure of Yang-Mills theory, fiber bundles, connections, and curvature. You have expertise in the geometric and topological aspects of gauge theories and their relationship to physics.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "statistical_mechanics",
                "systemPrompt": "You are a statistical mechanician specializing in the lattice models, phase transitions, and the connection between statistical mechanics and quantum field theory. You have expertise in the Osterwalder-Schrader axioms, reflection positivity, and the mass gap in lattice systems.",
                "model": "glm-5.1",
            },
            {
                "role": "contributor",
                "specialty": "formal_verification",
                "systemPrompt": "You are a formal verification expert specializing in Lean 4 and the formalization of mathematical physics. You have experience in formalizing operator algebras, Hilbert spaces, and the axiomatic structure of quantum field theories in proof assistants.",
                "model": "glm-5.1",
            },
        ],
    },
]


# ─── 千界花园 API 客户端 ───

class QianJieClient:
    """千界花园 HTTP API 客户端（零外部依赖，仅 urllib）。"""

    def __init__(self, base_url: str = QIANJIE_BASE_URL_DEFAULT):
        self.base_url = base_url
        self.timeout = 30

    def _request(self, method: str, endpoint: str, body: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        data = json.dumps(body).encode('utf-8') if body else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode('utf-8')
            except Exception:
                err_body = str(e)
            return {"success": False, "error": f"HTTP {e.code}: {err_body}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def health_check(self) -> Dict[str, Any]:
        try:
            return self._request("GET", "/api/research/sylva-sync")
        except Exception as e:
            return {"success": False, "error": str(e)}

    def init_millennium(self) -> Dict[str, Any]:
        """POST /api/research/millennium/init — 初始化千年难题生态。"""
        return self._request("POST", MILLENNIUM_INIT_ENDPOINT)

    def init_collaboration(self, domain: str, topic: str, collaboration_type: str) -> Dict[str, Any]:
        """POST /api/research/collaborations/init — 初始化协作。"""
        return self._request(
            "POST",
            "/api/research/collaborations/init",
            body={
                "domain": domain,
                "topic": topic,
                "collaborationType": collaboration_type,
            }
        )


# ─── 主流程 ───

def main():
    parser = argparse.ArgumentParser(description='Initialize Millennium Problem research ecosystem in QianJie')
    parser.add_argument('--qianjie-url', default=QIANJIE_BASE_URL_DEFAULT, help='QianJie base URL')
    parser.add_argument('--output-dir', default='config', help='Output directory for local JSON fallback')
    parser.add_argument('--skip-api', action='store_true', help='Skip API calls, save local JSON only')
    parser.add_argument('--init-all', action='store_true', help='Also initialize all 5 collaboration types for each problem')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = QianJieClient(args.qianjie_url)

    # 1. 检查千界花园可用性
    if not args.skip_api:
        print(f"[Phase 1] Checking QianJie at {args.qianjie_url}...")
        health = client.health_check()
        if health.get("success"):
            print("  -> QianJie is available!")
        else:
            print(f"  -> QianJie not available: {health.get('error', 'unknown')}")
            print("  -> Will save configurations to local JSON.")
            args.skip_api = True
    else:
        print("[Phase 1] --skip-api set, using local JSON only.")

    # 2. 调用千界花园 millennium/init
    if not args.skip_api:
        print("[Phase 2] POST /api/research/millennium/init...")
        result = client.init_millennium()
        if result.get("success"):
            data = result.get("data", {})
            problems = data.get("problems", [])
            print(f"  -> Successfully initialized {len(problems)} millennium problems!")
            for p in problems:
                print(f"     - {p.get('problemName', 'unknown')}: panel={p.get('panelId', 'N/A')}, tasks={p.get('taskCount', 0)}")
            # 同时保存结果到本地
            result_path = output_dir / f"millennium_init_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"  -> Result saved: {result_path}")
        else:
            print(f"  -> millennium/init failed: {result.get('error', 'unknown')}")
            print("  -> Falling back to local JSON.")
            args.skip_api = True

    # 3. 初始化协作类型（如果 --init-all）
    if args.init_all and not args.skip_api:
        print("[Phase 3] Initializing collaboration types for each problem...")
        collaboration_types = [
            "full_research",
            "theorem_proving",
            "paper_writing",
            "peer_review",
            "educational",
        ]
        for problem in MILLENNIUM_PROBLEMS:
            for collab_type in collaboration_types:
                print(f"  -> {problem['name']}: {collab_type}...", end=" ")
                result = client.init_collaboration(
                    domain=problem["domain"],
                    topic=problem["name"],
                    collaboration_type=collab_type,
                )
                if result.get("success"):
                    print("OK")
                else:
                    print(f"FAIL ({result.get('error', 'unknown')[:40]})")
                time.sleep(0.3)

    # 4. 保存本地配置（fallback 或备份）
    print("[Phase 4] Saving configurations to local JSON...")

    config = {
        "generated_at": datetime.now().isoformat(),
        "qianjie_url": args.qianjie_url,
        "problems": MILLENNIUM_PROBLEMS,
        "metadata": {
            "total_problems": len(MILLENNIUM_PROBLEMS),
            "total_experts": sum(len(p["experts"]) for p in MILLENNIUM_PROBLEMS),
            "domains": list(set(p["domain"] for p in MILLENNIUM_PROBLEMS)),
            "fields": list(set(p["field"] for p in MILLENNIUM_PROBLEMS)),
        }
    }

    config_path = output_dir / "millennium_problems.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"  -> Config: {config_path}")

    # 同时保存一个 "import-ready" 版本（直接可 POST 到 millennium/init）
    import_path = output_dir / "millennium_problems_import.json"
    with open(import_path, 'w', encoding='utf-8') as f:
        json.dump({"problems": MILLENNIUM_PROBLEMS}, f, ensure_ascii=False, indent=2)
    print(f"  -> Import-ready: {import_path}")

    # 保存每个问题的独立配置
    for problem in MILLENNIUM_PROBLEMS:
        prob_path = output_dir / f"millennium_{problem['id']}.json"
        with open(prob_path, 'w', encoding='utf-8') as f:
            json.dump(problem, f, ensure_ascii=False, indent=2)
    print(f"  -> Individual problem configs: {output_dir}/millennium_*.json")

    print(f"\n[Done] {len(MILLENNIUM_PROBLEMS)} millennium problems configured.")
    print(f"  Total experts: {config['metadata']['total_experts']}")
    print(f"  Domains: {', '.join(config['metadata']['domains'])}")
    print(f"  Fields: {', '.join(config['metadata']['fields'])}")
    if args.skip_api:
        print(f"\n  To import into QianJie, start the server and run:")
        print(f"    python scripts/millennium_init.py --qianjie-url {args.qianjie_url}")


if __name__ == '__main__':
    main()
