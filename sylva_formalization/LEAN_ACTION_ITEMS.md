# Sylva Formalization - Lean 代码任务清单

> **生成时间**: 2026-06-03  
> **状态追踪**: 本文件是 SylvaFormalization 项目所有可直接执行的 Lean 代码任务的中央清单。  
> **参考来源**: LEAN_NP_CLASS_STATUS.md | COOK_LEVIN_FORMALIZATION_TRACKER.md | 现有代码结构审计

---

## 一、项目现有模块审计

### 1.1 已有模块（标注状态）

| 模块 | 文件 | 状态 | 行数(约) | 备注 |
|------|------|------|----------|------|
| Basic | `Basic.lean` | ⚠️ 截肢版 | ~400 | 17个`sorry`，编码损坏后恢复 |
| Complexity | `Complexity.lean` | ⚠️ 占位符 | ~10 | 编码损坏，内容清空 |
| BSD | `BSD.lean` | ✅ 可用 | ~800 | 未审计 |
| EllipticCurveReduction | `EllipticCurveReduction.lean` | ✅ 可用 | ~500 | 未审计 |
| NavierStokes | `NavierStokes.lean` / `NavierStokes_fixed.lean` | ⚠️ 需修复 | ~1800 | 有fixed版本 |
| CP004 | `CP004.lean` / `CP004_B2.lean` | ⚠️ 多版本混乱 | ~1500 | 需合并整理 |
| ZetaVerifier | `ZetaVerifier.lean` / `ZetaVerifier_fixed.lean` | ✅ 可用 | ~1200 | fixed版本可用 |
| RiemannHypothesis | `RiemannHypothesis.lean` / `RiemannHypothesis_fixed.lean` | ✅ 可用 | ~1500 | fixed版本可用 |
| CookLevin | `CookLevin.lean` | ❌ 占位符 | ~10 | 编码损坏，内容清空 |
| SylvaInfrastructure | `SylvaInfrastructure.lean` | ✅ 可用 | ~2800 | 结构完整 |
| MathAgent | `MathAgent.lean` | ✅ 可用 | ~2800 | 未审计 |
| LocalGlobal | `LocalGlobal.lean` | ⚠️ 需修复 | ~2000 | 有amputated版本 |
| NumericalZeros | `NumericalZeros.lean` | ❌ 损坏 | ~1400 | noncomputable issues，被entry point注释掉 |
| Hodge | *(缺失)* | ❌ 缺失 | - | typeclass synthesis failures，被entry point注释掉 |
| QFT | `QFT.lean` | ✅ 存在 | - | 未审计完整性 |
| QuantumArithmetic | `QuantumArithmetic.lean` | ✅ 存在 | - | 未审计完整性 |
| Superconductivity_Pairing_Framework | `Superconductivity_Pairing_Framework.lean` | ⚠️ 需检查 | - | 有amputated版本 |
| StatisticalMechanics | `StatisticalMechanics.lean` | ✅ 存在 | - | 未审计 |
| RadiationTracker | `RadiationTracker.lean` | ✅ 存在 | - | 未审计 |
| PvsNP | `PvsNP/RazborovSmolensky.lean` | ✅ 存在 | - | 部分完成 |

### 1.2 缺失模块清单

- `Hodge.lean` - 已从 entry point 移除，需要重建
- `SATSolver.lean` - 从未创建
- `NPClass.lean` - 从未创建（Complexity.lean 中无实质NP定义）
- `FifteenConstants.lean` - 从未创建
- `ChernNumber.lean` - 从未创建
- `CookLevin_Reduction.lean` - 从未创建（CookLevin.lean 无实质内容）

---

## 二、任务清单（按难度排序）

### 🟢 易（1-2天）—— 利用现有 mathlib 基础设施的直接形式化

---

#### 任务 1: GF(3) 基本运算的完整证明回填

| 字段 | 内容 |
|------|------|
| **任务名** | GF(3) 运算律完整证明 |
| **难度** | 🟢 易 |
| **依赖** | Mathlib (`Fin n` 基础) |
| **参考来源** | 现有 `Basic.lean` 中的 `sorry` 标记; [Fin基础理论](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Fin/Basic.html) |
| **预估行数** | ~200 |
| **建议代码片段** | ```lean\ntheorem elems : (Finset.univ : Finset GF3) = {0, 1, 2} := by\n  ext x\n  fin_cases x <;> simp [GF3]\n``` |
| **文件路径** | `SylvaFormalization/Basic.lean` |

**详细说明**: 现有 Basic.lean 有 17 个 `sorry`，主要是 GF(3) 上的运算律（加法结合律、乘法结合律等）和黄金分割比 phi 的基本性质。这些在 mathlib 中已有完整基础设施，只需调用 `aesop` 或 `norm_num` 完成证明。

---

#### 任务 2: 多项式时间谓词 `IsPolynomial` 在 Lean 中的定义

| 字段 | 内容 |
|------|------|
| **任务名** | `IsPolynomial` 谓词形式化 |
| **难度** | 🟢 易 |
| **依赖** | Mathlib (`Polynomial` 库, `Nat` 上的渐近记法) |
| **参考来源** | [KrystianYC PR #35366](https://github.com/leanprover-community/mathlib4/issues/35366) 第 1-3 节; [Simas 2026 arXiv:2601.15571](https://arxiv.org/abs/2601.15571) |
| **预估行数** | ~150 |
| **建议代码片段** | ```lean\nimport Mathlib.Computability.TuringMachine\n\ndef IsPolynomial (f : ℕ → ℕ) : Prop :=\n  ∃ p : Polynomial ℕ, ∀ n, f n ≤ p.eval n\n\nlemma poly_add_poly : IsPolynomial f → IsPolynomial g → IsPolynomial (λ n => f n + g n) := ...\n``` |
| **文件路径** | `SylvaFormalization/NPClass/PolynomialTime.lean` |

**详细说明**: 这是 NP 类形式化的前置基础。mathlib 已有 `Polynomial` 和渐近记法，只需定义一个自然数函数是否被一个多项式上界控制。

---

#### 任务 3: 图灵机配置单步引理 `step_none_iff`

| 字段 | 内容 |
|------|------|
| **任务名** | TM1 `step_none_iff` 引理 |
| **难度** | 🟢 易 |
| **依赖** | Mathlib (`Turing.TM1` 模型) |
| **参考来源** | [KrystianYC PR #35366](https://github.com/leanprover-community/mathlib4/issues/35366) "Proposed PR sequence" PR 1; [PostTuringMachine.lean](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Computability/PostTuringMachine.html) |
| **预估行数** | ~50 |
| **建议代码片段** | ```lean\nimport Mathlib.Computability.PostTuringMachine\n\nlemma Turing.TM1.step_none_iff {Γ Λ σ} [Inhabited Γ] (M : Turing.TM1.machine Γ Λ σ)\n  (c : Turing.TM1.cfg Γ Λ σ) :\n  Turing.TM1.step M c = none ↔ c.l = none := by\n  cases c.l <;> simp [Turing.TM1.step]\n``` |
| **文件路径** | 作为 mathlib PR 提交，或 `SylvaFormalization/NPClass/TM1Complexity.lean` |

---

#### 任务 4: P ⊆ NP 定理形式化

| 字段 | 内容 |
|------|------|
| **任务名** | `p_sub_np` 定理 |
| **难度** | 🟢 易 |
| **依赖** | 任务 2 (IsPolynomial), 图灵机接受谓词定义 |
| **参考来源** | [KrystianYC PR #35366](https://github.com/leanprover-community/mathlib4/issues/35366); Sipser §7.3 |
| **预估行数** | ~100 |
| **建议代码片段** | ```lean\ntheorem p_sub_np {Γ} [Inhabited Γ] {accept : Γ → Prop}\n  (L : Language Γ) :\n  InP L accept → InNP L accept := by\n  intro hP\n  obtain ⟨M, p, hTime, hDecide⟩ := hP\n  use M, p\n  intro w hw\n  exact ⟨[], by simp, hDecide w hw⟩\n``` |
| **文件路径** | `SylvaFormalization/NPClass/Basic.lean` |

**详细说明**: P ⊆ NP 是教科书级别的平凡结果——如果一个语言能被多项式时间图灵机判定，那么用空证书作为NP证书即可。形式化非常直接。

---

#### 任务 5: 黄金分割比 phi 的核心恒等式库

| 字段 | 内容 |
|------|------|
| **任务名** | phi 恒等式批量证明 |
| **难度** | 🟢 易 |
| **依赖** | Mathlib (`Real.sqrt`, `norm_num`, `field_simp`) |
| **参考来源** | 现有 `Basic.lean` 中 phi 相关定义; [OEIS A001622](https://oeis.org/A001622) |
| **预估行数** | ~300 |
| **建议代码片段** | ```lean\nlemma phi_sq_eq_phi_add_one : phi^2 = phi + 1 := by\n  rw [phi]\n  nlinarith [Real.sqrt_pos.mpr (by norm_num : (5 : ℝ) > 0), Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ (5 : ℝ))]\n``` |
| **文件路径** | `SylvaFormalization/Basic.lean` (回填现有 sorry) |

---

### 🟡 中（1-2周）—— 需要移植或修改外部代码的形式化

---

#### 任务 6: NP 类完整定义（借鉴 KrystianYC）

| 字段 | 内容 |
|------|------|
| **任务名** | `InP` / `InNP` 类定义 + `DecidableInTime` |
| **难度** | 🟡 中 |
| **依赖** | 任务 2, 3; mathlib `Turing.TM1` |
| **参考来源** | [KrystianYC PR #35366](https://github.com/leanprover-community/mathlib4/issues/35366); [KrystianYC 完整代码](https://github.com/KrystianYCSilva/cli-and-ai/blob/main/prompt_os_lean/agente_matematico/AgenteMatematico/MathComplexityContrib.lean); Sipser §7.2-7.3 |
| **预估行数** | ~800 |
| **建议代码片段** | ```lean\n/-- Machine decides language within time bound --/\nstructure DecidableInTime {Γ Λ σ} [Inhabited Γ]\n  (M : Turing.TM1.machine Γ Λ σ) (L : Language Γ)\n  (accept : Γ → Prop) (T : ℕ → ℕ) : Prop where\n  time_bound : ∀ w, T w ≤ T w  -- placeholder\n  decide : ∀ w, w ∈ L ↔ acceptsAt M w accept\n\ndef InP {Γ} [Inhabited Γ] (L : Language Γ) (accept : Γ → Prop) : Prop :=\n  ∃ M p, IsPolynomial p ∧ DecidableInTime M L accept p\n\ndef InNP {Γ} [Inhabited Γ] (L : Language Γ) (accept : Γ → Prop) : Prop :=\n  ∃ M p c, IsPolynomial p ∧\n    ∀ w, w ∈ L ↔ ∃ cert, c w ≤ c w ∧ acceptsAt M (w, cert) accept\n``` |
| **文件路径** | `SylvaFormalization/NPClass/Basic.lean` |

**详细说明**: 这是 Sylva 项目的核心目标之一。KrystianYC 已有完整实现（零 sorry），但需要：
1. 适配 mathlib v4.28.0+ 的 API 变化
2. 整理为符合 mathlib 代码风格的结构
3. 完成 `runN` 燃料执行器及其引理（`runN_stable`, `runN_comp`, `runN_eq_of_halted`）

---

#### 任务 7: `runN` 燃料执行器 + 核心引理

| 字段 | 内容 |
|------|------|
| **任务名** | TM1 燃料执行器 `runN` |
| **难度** | 🟡 中 |
| **依赖** | 任务 3; mathlib `Turing.TM1` |
| **参考来源** | [KrystianYC PR #35366](https://github.com/leanprover-community/mathlib4/issues/35366) "Proposed PR sequence" PR 2; [PostTuringMachine.lean](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Computability/PostTuringMachine.html) |
| **预估行数** | ~400 |
| **建议代码片段** | ```lean\ndef Turing.TM1.runN {Γ Λ σ} [Inhabited Γ]\n  (M : Turing.TM1.machine Γ Λ σ) : ℕ → Turing.TM1.cfg Γ Λ σ → Turing.TM1.cfg Γ Λ σ\n| 0, c => c\n| n+1, c => match step M c with\n  | none => c\n  | some c' => runN M n c'\n\nlemma runN_stable {M n c} :\n  step M c = none → runN M n c = c := ...\n\nlemma runN_comp {M a b c} :\n  runN M (a + b) c = runN M b (runN M a c) := ...\n``` |
| **文件路径** | `SylvaFormalization/NPClass/TM1Complexity.lean` |

---

#### 任务 8: Cook-Levin 定理 — SAT 编码模块（移植自 Coq）

| 字段 | 内容 |
|------|------|
| **任务名** | TM1 → SAT 多项式归约 |
| **难度** | 🟡 中 |
| **依赖** | 任务 6, 7; Lean 命题逻辑基础 |
| **参考来源** | [uds-psl/cook-levin (Coq)](https://github.com/uds-psl/cook-levin); [Gäher & Kunze ITP 2021](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2021.20); Sipser §7.4 |
| **预估行数** | ~1500 |
| **建议代码片段** | ```lean\n/-- Encode a TM1 configuration as a Boolean formula --/\ndef encodeConfig {Γ Λ σ} [Fintype Γ] [Fintype Λ] [Fintype σ]\n  (c : Turing.TM1.cfg Γ Λ σ) : PropForm := ...\n\n/-- The Cook-Levin tableau formula: a 2D grid of configurations --/\ndef tableauFormula {Γ Λ σ} [Fintype Γ] [Fintype Λ] [Fintype σ]\n  (M : Turing.TM1.machine Γ Λ σ) (input : List Γ) (T : ℕ) : PropForm := ...\n\ntheorem cook_levin_reduction {Γ Λ σ} [Fintype Γ] [Fintype Λ] [Fintype σ]\n  {M : Turing.TM1.machine Γ Λ σ} {w : List Γ} {T : ℕ} :\n  (∃ c, Turing.TM1.Reaches (M, w) c ∧ c.halted) ↔\n  satisfiable (tableauFormula M w T) := ...\n``` |
| **文件路径** | `SylvaFormalization/CookLevin/Reduction.lean` |

**详细说明**: 从 Coq 移植 Cook-Levin 的核心难点：
1. Coq 使用 L-演算作为计算模型，而 Sylva 基于 mathlib 的 TM1
2. 需要将 Coq 的 `PropForm` 类型和可满足性定义迁移到 Lean
3. 保持多项式时间界限的形式化证明（Gäher & Kunze 的关键创新）

**外部参考**:
- Coq 代码: https://github.com/uds-psl/cook-levin
- 论文: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2021.20
- ITP 2021 视频/补充材料: https://www.ps.uni-saarland.de/~gaeher/cook-levin/

---

#### 任务 9: 15 常数统一关系的形式化（第一阶段）

| 字段 | 内容 |
|------|------|
| **任务名** | 15 常数间代数关系的形式化 |
| **难度** | 🟡 中 |
| **依赖** | 任务 5 (phi 基础); `Real`, `Complex` 运算 |
| **参考来源** | `sylva_academic/15_constants_data.md`; [论文材料](https://vixra.org/abs/2504.0139) |
| **预估行数** | ~600 |
| **建议代码片段** | ```lean\nimport Mathlib\n\nnamespace FifteenConstants\n\n-- 核心统一常数：phi 出现的位置\ndef alpha_GUT_inv : ℝ := 137 + delta\nlemma alpha_GUT_inv_phi_relation :\n  alpha_GUT_inv = 137 + phi - 1 / phi := by ...\n\n-- 精细结构常数与 phi 的关系（猜想级）\ndef alpha_obs_inv_approx : ℝ := 137.035999\nlemma alpha_obs_phi_relation (h : alpha_obs_inv_approx = alpha_GUT_inv - correction) :\n  correction > 0 := by ...\n\nend FifteenConstants\n``` |
| **文件路径** | `SylvaFormalization/FifteenConstants/AlgebraicRelations.lean` |

**详细说明**: 15 常数统一的核心是发现它们之间的数值巧合和代数关系。第一阶段先形式化已知的精确关系（如 phi 与 GUT 耦合的级数展开），第二阶段再处理近似关系。

---

#### 任务 10: SAT 求解器 DPLL 算法的描述形式化

| 字段 | 内容 |
|------|------|
| **任务名** | DPLL / CDCL SAT 求解器 Lean 描述 |
| **难度** | 🟡 中 |
| **依赖** | 命题逻辑形式化 (PropForm); mathlib `List`, `Finset` |
| **参考来源** | [Lescuyer & Conchon 2008](https://api.semanticscholar.org/CorpusID:6321766); [Marques-Silva SAT checker in Coq](https://bfischer.pages.cs.sun.ac.za/pdfs/coq-09.preprint.pdf); [SAT solver verification survey](https://matryoshka-project.github.io/pubs/sat_article.pdf) |
| **预估行数** | ~1000 |
| **建议代码片段** | ```lean\ninductive Literal (V : Type) :=\n| pos (v : V)\n| neg (v : V)\n\ndef Clause (V : Type) := List (Literal V)\ndef CNF (V : Type) := List (Clause V)\n\n/-- DPLL algorithm (functional version) --/\ndef dpll {V} [DecidableEq V] [Fintype V] :\n  CNF V → PartialAssignment V → Bool\n| [], _ => true\n| (c :: cs), assign =>\n  if c.isSatisfied assign then dpll cs assign\n  else if c.isContradictory assign then false\n  else match c.pickLiteral assign with\n    | some l =>\n      dpll (c :: cs) (assign.assign l) ||\n      dpll (c :: cs) (assign.assign l.negate)\n    | none => false\n\nlemma dpll_sound {V} [DecidableEq V] [Fintype V]\n  (f : CNF V) (assign : PartialAssignment V) :\n  dpll f assign = true → satisfiable f := ...\n``` |
| **文件路径** | `SylvaFormalization/SATSolver/DPLL.lean` |

**详细说明**: 这是为 Cook-Levin 的反向验证做准备（SAT ∈ NP）。先形式化 DPLL 算法的功能描述及其正确性，后续可扩展为 CDCL 并加入 Two-Watched-Literal 优化。

---

#### 任务 11: SylvaInfrastructure 的接口完整实现

| 字段 | 内容 |
|------|------|
| **任务名** | 基础设施接口完整化 |
| **难度** | 🟡 中 |
| **依赖** | 现有 `SylvaInfrastructure.lean` / `SylvaInfrastructure_interface.lean` |
| **参考来源** | 现有 `SylvaInfrastructure_final.lean` (backup); `SylvaFormalization.lean` entry point |
| **预估行数** | ~500 |
| **建议代码片段** | ```lean\nstructure SylvaInterface where\n  query : String → IO String\n  prove : Expr → TacticM Unit\n  verify : String → IO Bool\n  -- 统一接入所有形式化模块\n``` |
| **文件路径** | `SylvaFormalization/SylvaInfrastructure.lean` |

---

### 🔴 难（1-3月）—— 需要重大理论工作的形式化

---

#### 任务 12: Cook-Levin 定理完整证明（Lean）

| 字段 | 内容 |
|------|------|
| **任务名** | SAT NP-完全性完整形式化 |
| **难度** | 🔴 难 |
| **依赖** | 任务 6, 7, 8, 10; P ⊆ NP (任务 4); 多项式归约传递性 |
| **参考来源** | [uds-psl/cook-levin](https://github.com/uds-psl/cook-levin); [Gäher & Kunze ITP 2021](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2021.20) (arXiv: 2601.15571 补充); Sipser §7.4 |
| **预估行数** | ~5000 |
| **建议代码片段** | ```lean\n-- 完整定理陈述\ntheorem SAT_is_NPComplete :\n  IsNPComplete SAT :=\n  ⟨SAT_in_NP, SAT_is_NPHard⟩\n\nwhere\n  SAT_in_NP : InNP SAT acceptsSat := ...  -- 用 DPLL 证书验证器\n  SAT_is_NPHard : ∀ L, InNP L accept → PolynomialTimeReducible L SAT := ...  -- Cook-Levin 归约\n``` |
| **文件路径** | `SylvaFormalization/CookLevin/Theorem.lean` |

**详细说明**: 这是整个 Sylva 项目的核心目标之一。完整形式化需要：
1. 构造从任意 NP 问题到 SAT 的多项式归约（Cook-Levin 的构造性证明）
2. 证明归约函数的 PolynomialTime 属性（资源分析是 Gäher & Kunze 的核心创新）
3. 证明归约的正确性（TM1 接受 ↔ 公式可满足）
4. 证明 SAT ∈ NP（通过 DPLL 证书验证器）

**里程碑**:
- [ ] 完成 TM1 → SAT 编码函数定义
- [ ] 证明编码函数多项式时间可计算
- [ ] 证明编码正确性（前向/后向）
- [ ] 完成 SAT ∈ NP
- [ ] 组装为 `IsNPComplete SAT`

---

#### 任务 13: 陈数计算（Chern Number Formalization）

| 字段 | 内容 |
|------|------|
| **任务名** | 第一陈数完整形式化 |
| **难度** | 🔴 难 |
| **依赖** | mathlib `Manifold`, `FiberBundle`, `deRham`（部分）; 拓扑学形式化 |
| **参考来源** | [Mathlib Topology 文档](https://www.imo.universite-paris-saclay.fr/~patrick.massot/mil/07_Topology.html); [Chern number on closed surfaces](https://eprints.lancs.ac.uk/id/eprint/152064/1/2020KRipsMRes.pdf); [Real-space Chern number PRB 2023](https://link.aps.org/doi/10.1103/PhysRevB.108.174204); [Lin et al. arXiv:2603.05616](https://arxiv.org/pdf/2603.05616) |
| **预估行数** | ~5000 |
| **建议代码片段** | ```lean\nimport Mathlib.Geometry.Manifold.VectorBundle.Basic\n\nvariable {M : Type*} [TopologicalSpace M] [ChartedSpace ℝ^n M] [SmoothManifoldWithCorners 𝓘(ℝ, ℝ^n) M]\n\n/-- First Chern class of a complex line bundle --/\nnoncomputable def firstChernClass (E : VectorBundle ℂ (Fin 1) M) :\n  H^2(M; ℤ) := ...\n\n/-- Chern number as integral of curvature --/\nnoncomputable def chernNumber (E : VectorBundle ℂ (Fin 1) M) : ℤ :=\n  ∫ x, curvature E x / (2 * π)\n\ntheorem chernNumber_is_integer : chernNumber E ∈ Set.range (λ n : ℤ => (n : ℝ)) := ...\n``` |
| **文件路径** | `SylvaFormalization/ChernNumber/Basic.lean` |

**详细说明**: 陈数是 Sylva 项目统一 15 常数时的关键拓扑不变量。形式化需要：
1. mathlib 中尚未完整的上同调理论（特别是 de Rham 上同调与 Čech 上同调的同构）
2. 复向量丛的连接和曲率形式化
3. 数值计算版本（格点求和）与连续版本的等价性证明
4. 与欧拉示性数的关系（Gauss-Bonnet 定理）

**外部参考**:
- 已有 15,000 行 Lean 代码（非 mathlib 风格）需重构
- mathlib PR #9550 (triangulated structure on homotopy category) 显示了类似的上同调形式化路径
- [Hal-04546712](https://hal.science/hal-04546712v2/file/derived-categories.pdf) 中的导出范畴形式化（J. Riou）提供了高层架构参考

---

#### 任务 14: Hodge 猜想的形式化骨架重建

| 字段 | 内容 |
|------|------|
| **任务名** | Hodge Conjecture 骨架形式化 |
| **难度** | 🔴 难 |
| **依赖** | 任务 13 (陈数/陈类); 代数几何基础 (`AlgebraicGeometry` in mathlib); 复流形 |
| **参考来源** | [Hodge Conjecture (Clay Math Institute)](https://www.claymath.org/millennium-problems/hodge-conjecture); [Mathlib AlgebraicGeometry](https://leanprover-community.github.io/mathlib4_docs/Mathlib/AlgebraicGeometry.html) |
| **预估行数** | ~3000 |
| **建议代码片段** | ```lean\n/-- Hodge decomposition for a compact Kähler manifold --/\ndef HodgeDecomposition {X : Type*} [CompactSpace X] [KählerManifold X]\n  (k : ℕ) :\n  H^k(X, ℂ) ≅ DirectSum (λ (p q : ℕ) (_ : p + q = k) => H^{p,q}(X)) := ...\n\n/-- The Hodge Conjecture statement --/\ndef HodgeConjecture : Prop :=\n  ∀ {X : Type*} [ProjectiveVariety X] [Smooth X],\n  ∀ k,\n  ∀ α ∈ H^{k,k}(X, ℚ) ∩ H^{2k}(X, ℚ),\n  ∃ Z : AlgebraicCycle X k,\n  [Z] = α\n``` |
| **文件路径** | `SylvaFormalization/Hodge/HodgeConjecture.lean` |

**详细说明**: Hodge 猜想是 Clay 千禧年大奖难题之一。形式化需要大量前置工作：
1. 复流形上的 Hodge 分解（mathlib 中尚未完成）
2. 代数闭链（Algebraic Cycle）的定义
3. 霍奇类与代数闭链的对应关系
当前 mathlib 的 `AlgebraicGeometry` 已初具规模，但远未覆盖复代数几何的层面。

---

#### 任务 15: P ≠ NP 猜想的形式化陈述

| 字段 | 内容 |
|------|------|
| **任务名** | `PNeNP` 命题形式化 |
| **难度** | 🔴 难 |
| **依赖** | 任务 6 (NP 类完整定义); 分离论证框架 |
| **参考来源** | [KrystianYC PR #35366](https://github.com/leanprover-community/mathlib4/issues/35366); [Razborov-Rudich Natural Proofs](https://arxiv.org/abs/cs/0502034); [Simas 2026 arXiv:2601.15571](https://arxiv.org/abs/2601.15571) |
| **预估行数** | ~2000 |
| **建议代码片段** | ```lean\n/-- The P vs NP problem as a formal proposition --/\ndef PNeNP : Prop := ¬(∀ {Γ} [Inhabited Γ] {accept},\n  ∀ L, InP L accept ↔ InNP L accept)\n\n/-- P ≠ NP implies no polynomial-time SAT solver exists --/\ntheorem pne_np_implies_no_poly_sat_solver\n  (h : PNeNP) :\n  ¬∃ (solver : CNF String → Bool),\n    IsPolynomialTime solver ∧\n    ∀ f, solver f = true ↔ satisfiable f := ...\n``` |
| **文件路径** | `SylvaFormalization/PvsNP/PNeNP.lean` |

**详细说明**: 形式化 P ≠ NP 的陈述相对直接（任务 6 完成后即可定义），但为其提供任何非平凡的形式化证据（如电路复杂性下界）则极其困难。此任务的重点是：
1. 定义清晰的命题陈述
2. 建立与其他计算复杂性结果的蕴含关系
3. 形式化 Razborov-Rudich "Natural Proofs" 障碍（说明为何某些证明技术不可能成功）
4. 为 Sylva 的 "描述复杂度" 方法预留接口

**外部参考**:
- 现有 `PvsNP/RazborovSmolensky.lean` 可能已有部分电路复杂性工作
- [Razborov-Smolensky 定理 (arXiv)](https://arxiv.org/abs/cs/0502034)

---

#### 任务 16: 15 常数统一关系的完整物理推导形式化

| 字段 | 内容 |
|------|------|
| **任务名** | 15 常数从第一原理推导的骨架 |
| **难度** | 🔴 难 |
| **依赖** | 任务 13 (陈数); 任务 9 (代数关系); 规范场论基础 |
| **参考来源** | `sylva_academic/15_constants_data.md`; [Sylva TOE 论文](https://vixra.org/abs/2504.0139); [Sylva Berry-Keating 分析](sylva_academic/BERRY_KEATING_RH_DEEP.md) |
| **预估行数** | ~8000 |
| **建议代码片段** | ```lean\n-- 从陈数推导精细结构常数（猜想框架）\ntheorem alpha_from_chern_and_geometry\n  {M : Type*} [Spacetime M]\n  (h1 : firstChernClass (gaugeBundle M) = 3)  -- 从三世代导出\n  (h2 : eulerCharacteristic M = -6) :\n  α_GUT⁻¹ = 137 := by ...  -- 需要大量物理假设\n\n-- 精细结构常数的 phi 修正\ntheorem alpha_obs_correction\n  (h : α_GUT⁻¹ = 137) :\n  α_obs⁻¹ = 137 + φ - 1/φ - quantum_corrections := ...\n``` |
| **文件路径** | `SylvaFormalization/FifteenConstants/Derivation.lean` |

**详细说明**: 这是 Sylva 项目的终极目标。形式化 15 常数统一需要：
1. 建立规范场论中耦合常数与拓扑不变量的关系（Chern-Simons 理论形式化）
2. 重正化群方程的形式化（从 GUT 能标到观测能标的跑动）
3. 数值计算验证（`norm_num` 在物理常数精度上的应用）
4. 明确标注哪些是严格定理、哪些是物理假设/近似

---

### ⚫ 极难（3月+）—— 依赖未证明猜想的形式化

---

#### 任务 17: 黎曼猜想完整证明（或等价陈述）的形式化

| 字段 | 内容 |
|------|------|
| **任务名** | Riemann Hypothesis 形式化 |
| **难度** | ⚫ 极难 |
| **依赖** | mathlib `ZetaFunction` 完善; 解析数论大量基础 |
| **参考来源** | [Mathlib Zeta Function](https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/ZetaFunction.html); [de Bruijn formalization approaches](https://arxiv.org/abs/2311.15377); [Sylva Berry-Keating 分析](sylva_academic/BERRY_KEATING_RH_DEEP.md) |
| **预估行数** | ~20000+ |
| **建议代码片段** | ```lean\n/-- The Riemann Hypothesis as a formal proposition --/\ndef RiemannHypothesis : Prop :=\n  ∀ s : ℂ, riemannZeta s = 0 → (s.re = 1/2 ∨ s.re < 0 ∨ s.re > 1)\n  -- 等价：非平凡零点实部均为 1/2\n``` |
| **文件路径** | `SylvaFormalization/RiemannHypothesis/Statement.lean` |

**详细说明**: 黎曼猜想是 Clay 千禧年难题之一。当前 mathlib 已有 `riemannZeta` 和 `riemannCompletedZeta` 的定义，但远未覆盖证明所需的解析数论工具。Sylva 的 Berry-Keating 方法（量子混沌与谱对应）提供了一条独特的形式化路径，但需要：
1. 随机矩阵理论的形式化
2. 量子哈密顿量与 ζ 零点的对应
3. Gutzwiller 迹公式的严格版本

**当前状态**: 现有 `RiemannHypothesis.lean` 和 `RiemannHypothesis_fixed.lean` 可能只包含骨架陈述，需审计。

---

#### 任务 18: Navier-Stokes 存在性与光滑性问题形式化

| 字段 | 内容 |
|------|------|
| **任务名** | Navier-Stokes Existence and Smoothness |
| **难度** | ⚫ 极难 |
| **依赖** | mathlib `NavierStokes` 完善; Sobolev 空间; 偏微分方程理论 |
| **参考来源** | [Clay Math Institute Navier-Stokes Problem](https://www.claymath.org/millennium-problems/navier-stokes-equation); [Mathlib PDE 发展](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/PDE.html) |
| **预估行数** | ~30000+ |
| **建议代码片段** | ```lean\n/-- Weak solution to 3D incompressible Navier-Stokes --/\nstructure WeakSolution where\n  u : ℝ³ × ℝ → ℝ³\n  p : ℝ³ × ℝ → ℝ\n  regularity : u ∈ L^2(0,T; H^1(ℝ³)) ∩ L^∞(0,T; L^2(ℝ³))\n  ...\n\n/-- Millennium Prize Problem statement --/\ndef NavierStokesMillennium : Prop :=\n  ∀ (u₀ : ℝ³ → ℝ³), u₀ ∈ C^∞_c(ℝ³) → div u₀ = 0 →\n  ∃ (u p), WeakSolution u₀ u p ∧\n  u ∈ C^∞(ℝ³ × [0,∞))\n``` |
| **文件路径** | `SylvaFormalization/NavierStokes/MillenniumProblem.lean` |

**详细说明**: 另一个 Clay 千禧年难题。mathlib 的 PDE 理论仍在早期阶段，Sobolev 空间、Navier-Stokes 弱解理论均不完整。现有 `NavierStokes.lean` 可能只包含简化版本。

---

#### 任务 19: Birch-Swinnerton-Dyer 猜想完整形式化

| 字段 | 内容 |
|------|------|
| **任务名** | BSD Conjecture 完整陈述 |
| **难度** | ⚫ 极难 |
| **依赖** | 椭圆曲线算术; L-函数; Galois 表示; 模形式 |
| **参考来源** | [Clay Math Institute BSD Problem](https://www.claymath.org/millennium-problems/birch-and-swinnerton-dyer-conjecture); [Mathlib EllipticCurve](https://leanprover-community.github.io/mathlib4_docs/Mathlib/AlgebraicGeometry/EllipticCurve/Basic.html) |
| **预估行数** | ~25000+ |
| **建议代码片段** | ```lean\n/-- BSD Conjecture: rank equals analytic rank --/\ndef BSDConjecture (E : EllipticCurve ℚ) : Prop :=\n  E.rank = E.analyticRank ∧\n  E.sha.card = E.bsdFormula / (E.regulator * E.torsionOrder * E.period * E.tamagawaProduct)\n``` |
| **文件路径** | `SylvaFormalization/BSD/Conjecture.lean` |

**详细说明**: BSD 猜想的完整形式化需要 L-函数理论、模形式、Galois 上同调等大量前置工作。mathlib 已有椭圆曲线基础定义，但远未覆盖 BSD 所需的深度。

---

## 三、优先级建议与路线图

### Phase 1（第 1-2 周）：基础修复与形式化启动
1. 任务 1: GF(3) 回填（解锁 Basic 模块编译）
2. 任务 2: `IsPolynomial` 定义（解锁复杂性理论模块）
3. 任务 3: `step_none_iff`（解锁 TM1 复杂性扩展）
4. 任务 5: phi 恒等式库（解锁 15 常数模块）

### Phase 2（第 3-6 周）：NP 类与 Cook-Levin 核心
5. 任务 6: NP 类完整定义
6. 任务 7: `runN` 燃料执行器
7. 任务 4: P ⊆ NP 证明
8. 任务 8: Cook-Levin SAT 编码（移植开始）

### Phase 3（第 7-12 周）：Cook-Levin 完成与扩展
9. 任务 10: SAT 求解器 DPLL 形式化
10. 任务 12: Cook-Levin 完整定理（组装）
11. 任务 9: 15 常数代数关系（第一阶段）
12. 任务 11: SylvaInfrastructure 接口完整化

### Phase 4（第 13-24 周）：高级数学物理模块
13. 任务 13: 陈数计算（分阶段）
14. 任务 14: Hodge 骨架重建
15. 任务 15: P ≠ NP 陈述与障碍形式化

### Phase 5（长期）：千禧年难题框架
16. 任务 16: 15 常数完整推导
17. 任务 17: 黎曼猜想（Berry-Keating 路径）
18. 任务 18: Navier-Stokes
19. 任务 19: BSD

---

## 四、外部参考索引

### GitHub 仓库
| 名称 | 链接 | 用途 |
|------|------|------|
| KrystianYC 复杂性形式化 | https://github.com/KrystianYCSilva/cli-and-ai/blob/main/prompt_os_lean/agente_matematico/AgenteMatematico/MathComplexityContrib.lean | NP类、runN、P⊆NP |
| uds-psl/cook-levin | https://github.com/uds-psl/cook-levin | Cook-Levin Coq移植源 |
| mathlib4 (官方) | https://github.com/leanprover-community/mathlib4 | 基础库 |
| mathlib4 PR #35366 | https://github.com/leanprover-community/mathlib4/issues/35366 | NP类贡献讨论 |
| mathlib4 PR #33132 | https://github.com/leanprover-community/mathlib4/pull/33132 | FinTM0复杂性 |
| mathlib4 PR #9550 | https://github.com/leanprover-community/mathlib4/pull/9550 | 三角范畴结构 |

### 论文与arXiv
| 标题 | 链接 | 用途 |
|------|------|------|
| Simas 2026 | arXiv:2601.15571 | 多项式时间归约 |
| Gäher & Kunze ITP 2021 | https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2021.20 | Cook-Levin机械化 |
| Lin et al. PRB 2023 | https://link.aps.org/doi/10.1103/PhysRevB.108.174204 | 实空间陈数 |
| Lin et al. arXiv | arXiv:2603.05616 | 陈数计算 |
| Lescuyer & Conchon SAT 2008 | https://api.semanticscholar.org/CorpusID:6321766 | SAT求解器形式化 |
| Riou 导出范畴 HAL | https://hal.science/hal-04546712v2/file/derived-categories.pdf | 范畴论参考 |
| Sylva 15常数论文 | https://vixra.org/abs/2504.0139 | 物理统一理论 |

### 教科书
| 书名 | 章节 | 用途 |
|------|------|------|
| Sipser, Introduction to the Theory of Computation | §3.1, §7.2-7.4 | 复杂性理论基础 |
| Sipser | §7.4 | Cook-Levin构造 |
| 需补充：Chern数相关微分几何教材 | - | 陈类与示性类 |

---

## 五、注意事项与风险

### 编码风险
- **历史问题**: 多次发生编码损坏导致模块截肢
- **缓解措施**: 所有新文件使用 UTF-8 编码，提交前用 `lake build` 验证

### mathlib API 变化
- mathlib 更新频繁，API 可能变化
- **缓解措施**: 锁定 mathlib 版本（当前 v4.28.0-rc1），定期升级

### 理论难度
- 红色/黑色任务依赖未完成的数学基础
- **缓解措施**: 优先完成绿色/黄色任务，建立可编译的骨架；对红色/黑色任务采用 "假设-结论" 分离模式（先形式化陈述，再逐步证明）

---

> **"Don't worry. Even if the world forgets, I'll remember for you."**  
> — Sylva  
> 
> 最后更新: 2026-06-03 by Subagent
