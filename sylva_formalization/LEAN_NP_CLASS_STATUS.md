# Lean 4 + Mathlib 中 NP类 / P类 / NP-Complete 的定义状态

**报告日期**: 2026-06-03  
**追踪范围**: Lean 4 / Mathlib 4 / Isabelle AFP / Coq 社区  
**关键词**: NP, P, NP-Complete, ComplexityClass, Cook-Levin, Turing Machine, Polynomial Time

---

## 1. 执行摘要 (Executive Summary)

**结论**: Mathlib4 目前**尚未正式收录** P、NP、NP-Complete 的完整定义和 Cook-Levin 定理的形式化证明。但**已有完整的独立实现**，状态如下：

| 项目 | 状态 | 位置/作者 |
|------|------|----------|
| P/NP 类定义 (基于 TM1) | ✅ 已完成，未合并 | Issue #35366, 作者: KrystianYC |
| 单带 TM 复杂度 | 🔄 有 PR 草案 | PR #33132, 作者: BoltonBailey |
| 多项式时间归约框架 | ✅ 独立发布 | Simas (2026), arXiv:2601.15571 |
| Cook-Levin 定理 | ✅ 外部项目完成 | Isabelle AFP (2025), Coq (ITP 2021) |
| Mathlib 基础 TM 模型 | ✅ 已存在 | `PostTuringMachine.lean` (Carneiro 2018) |

**核心差距**: Mathlib4 缺少**正式的 NP-Complete 定义**和**Cook-Levin 定理**的形式化。现有基础设施足以支持这些形式化，但尚未整合到主库。

---

## 2. 基础设施现状清单

### 2.1 已存在的 Mathlib4 基础设施

| 组件 | 文件路径 | 作者 | 状态 | 说明 |
|------|---------|------|------|------|
| **Post-Turing Machine (TM0/TM1)** | `Mathlib/Computability/PostTuringMachine.lean` | Mario Carneiro (2018) | ✅ 已合并 | 单带图灵机模型，`Turing.TM0`, `Turing.TM1` |
| **多带图灵机 (TM2)** | `Mathlib/Computability/TMComputable.lean` | 社区 | ✅ 已合并 | 多带 TM，`FinTM2`，时间复杂度定义 |
| **TM1 步数计数器 (`runN`)** | 独立实现 (Issue #35366) | KrystianYC | 🔄 待合并 | `runN : Nat → Cfg → Cfg` |
| **TM1 停机引理** | `Turing.TM1.step_none_iff` | KrystianYC | 🔄 待合并 | `step M c = none ↔ c.l = none` |
| **图灵机求值** | `Turing.eval`, `Turing.Reaches` | Carneiro | ✅ 已合并 | 无步数追踪的版本 |

### 2.2 现有基础设施的技术细节

#### TM0 模型 (`PostTuringMachine.lean`)

```lean
-- 简化示意
tm0 : machine Γ Λ  -- Λ: 状态标签, Γ: 磁带符号
step : Cfg → Option Cfg  -- 单步执行
Turing.eval : part (List Γ)  -- 求值输出
```

**特点**:
- 允许无限状态集（通过 `Inhabited` 约束）
- 通过 `Support` 概念处理有限性
- 无内置的接受/拒绝状态区分
- **无时间/步数追踪**

#### TM1 模型
- 在 TM0 基础上增加了更灵活的状态转换
- 同样缺乏时间复杂度基础设施

#### TM2 / `FinTM2` 模型 (`TMComputable.lean`)
- 多带图灵机
- 有 `EvalsToInTime` 的定义（基于结构的而非燃料的）
- **与 Issue #35366 的方案正交**

### 2.3 已验证的图灵机等价性

以下归约在 Mathlib4 中**已经形式化**（Carneiro 等）:

| 归约 | 状态 |
|------|------|
| TM1 ↔ TM0 | ✅ |
| TM1(Γ) → TM1(Bool) | ✅ |
| TM2 → TM1 | ✅ |
| TM1 ↔ TM2 的**多项式时间**等价 | ❌ 待完成 |

---

## 3. 独立实现与待合并工作

### 3.1 Issue #35366: P/NP 类定义 (KrystianYC, 2026-02-15)

**链接**: https://github.com/leanprover-community/mathlib4/issues/35366

**代码仓库**: https://github.com/KrystianYCSilva/cli-and-ai/blob/main/prompt_os_lean/agente_matematico/AgenteMatematico/MathComplexityContrib.lean

**贡献内容**:

| 组件 | 状态 |
|------|------|
| `Turing.TM1.runN` | ✅ 燃料型步数计数器 |
| `runN_stable` | ✅ 停机配置稳定性 |
| `runN_comp` | ✅ 组合性: `runN (a+b) = runN b ∘ runN a` |
| `IsPolynomial` | ✅ 多项式时间界限 |
| `DecidableInTime` | ✅ 机器在时间界限内判定语言 |
| **`InP` 类** | ✅ **P 复杂度类** |
| **`InNP` 类** | ✅ **NP 复杂度类** |
| **`p_sub_np`** | ✅ **P ⊆ NP (零 sorry)** |
| `PEqNP` / `PNeNP` | ✅ P=NP / P≠NP 的形式命题 |

**设计选择**:
- 基于 `Turing.TM1`（现有 Mathlib 模型）
- 使用**燃料型 (fuel-based)** `runN` 而非结构型 `EvalsTo`
- 接受状态通过磁带头部的谓词 `accept : Γ → Prop` 参数化（参考 Sipser §3.1）
- 通用字母表: `Γ : Type*` with `[Inhabited Γ]`

**质量**: 编译通过 Mathlib v4.28.0-rc1，零 `sorry`，零 lint 警告。

**状态**: 等待社区审查，尚未提交 PR。

### 3.2 PR #33132: 单带 TM 复杂度 (BoltonBailey)

**链接**: https://github.com/leanprover-community/mathlib4/pull/33132

**方案对比**:

| 特性 | Issue #35366 (KrystianYC) | PR #33132 (BoltonBailey) |
|------|--------------------------|-------------------------|
| 基础模型 | 现有 `Turing.TM1` | 新 `FinTM0` bundled type |
| 时间计数 | 燃料型 `runN` | 结构型 `EvalsToInTime` |
| 状态处理 | 参数化接受谓词 | bundled finiteness |
| 风格 | 扩展现有代码 | 新建类型体系 |

**状态**: PR #33132 为草案状态，与 Issue #35366 的方案**互补而非竞争**。

### 3.3 Simas (2026): 多项式时间归约框架

**论文**: "Computational Complexity of Physical Counting"  
**arXiv**: https://arxiv.org/abs/2601.15571  
**代码**: 28863 行 Lean 4，1252 定理/引理，113 文件，**零 sorry**

**特点**:
- 定义了 `PolyReduction` 结构体，包含 `runtime` 和 `size`
- 实现了多项式时间归约的**组合定理**
- **不使用 Mathlib 的 TM 模型**
- 不定义 P/NP 类，但定义了复杂度结果
- 所有复杂度结果以显式 Lean 定理参数形式携带假设

---

## 4. 缺失组件清单

### 4.1 核心缺失 (阻塞 Cook-Levin)

| 缺失组件 | 优先级 | 依赖 |
|---------|--------|------|
| **Cook-Levin 定理** | 🔴 最高 | NP 定义 + SAT 形式化 + 多项式归约 |
| **SAT 的形式化** | 🔴 最高 | 布尔公式编码 + 可满足性谓词 |
| **多项式时间归约 (≤ₚ)** | 🔴 最高 | P/NP 定义 + 编码理论 |
| **TM1 编码为布尔公式** | 🔴 最高 | 配置编码 + 转移函数编码 |
| **NP-Complete 定义** | 🟡 高 | NP 类 + ≤ₚ |
| **NP-Hard 定义** | 🟡 高 | ≤ₚ |
| **TM1 ↔ TM2 多项式等价** | 🟡 高 | 现有等价性 + 时间分析 |

### 4.2 辅助缺失

| 缺失组件 | 优先级 | 说明 |
|---------|--------|------|
| 字符串/列表的多项式时间编码 | 🟡 高 | 将输入编码为 TM 磁带 |
| 有限支持 TM 的标准化 | 🟡 中 | `FinTM1` 的定义 |
| 配置图的编码 | 🟡 中 | Cook-Levin 的表格法 |
| 电路复杂度 (Circuit Complexity) | 🟢 低 | 可选替代路径 |
| 非确定性 TM 模型 | 🟢 低 | 可用验证器+证书替代 |

---

## 5. 外部可参考的形式化

### 5.1 Isabelle AFP: Cook-Levin 定理 (2025)

**作者**: Christoph Weidenbach (Max Planck Institute)  
**链接**: https://devel.isa-afp.org/entries/Cook_Levin.html  
**年份**: 2025

**包含内容**:
- SAT 的形式化定义
- **P 类** 的形式化
- **NP 类** 的形式化
- **多项式时间多一归约** (≤ₚ)
- **P ⊆ NP** 的证明
- **Cook-Levin 定理** 的完整证明

**文件结构**:
```
Cook_Levin/
├── Time_Complexity.thy    -- 时间复杂度基础
├── Elementary.thy         -- 基本组件
├── Composing.thy        -- 组合理论
├── Symbol_Ops.thy        -- 符号操作
├── TM.thy                -- 图灵机
├── SAT.thy               -- 可满足性问题
├── NP.thy                -- NP 类 + P 类
├── Reductions.thy        -- 归约理论
└── Cook_Levin.thy        -- 主定理
```

**关键定义 (Isabelle)**:
```isabelle
type_synonym 'a word = "'a list"

definition time_bounded :: "(nat ⇒ nat) ⇒ machine ⇒ bool"
definition P :: "lang set"
definition NP :: "lang set"
definition polynomial_time_reduction :: ...
```

### 5.2 Coq: Mechanising Complexity Theory (ITP 2021)

**作者**: Lennard Gäher, Fabian Kunze (Universität des Saarlandes)  
**论文**: "Mechanising Complexity Theory: The Cook-Levin Theorem in Coq"  
**会议**: ITP 2021  
**链接**: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2021.20  
**代码**: https://github.com/uds-psl/cook-levin  
**引用数**: 17+

**创新点**:
- 使用 **call-by-value λ-演算 L** 作为计算模型（非 TM）
- L 与 TM 在多项式时间内等价
- 首次在**具体计算模型**上机械验证复杂度理论结果
- 使用 TM 作为 L→SAT 归约的**中间步骤**

**技术路径**:
```
L-computation → TM encoding → Boolean formula encoding
```

**关键文件**:
| 文件 | 内容 |
|------|------|
| `Time.v` | L-演算的时间复杂度 |
| `NP.v` | NP 类定义 |
| `ReducibleInTime.v` | 多项式时间归约 |
| `SAT.v` | SAT 定义 |
| `TM.v` | 图灵机编码 |
| `CookLevin.v` | 主定理 |

### 5.3 Isabelle AFP: 之前的复杂度工作

| 年份 | 作者 | 内容 |
|------|------|------|
| 2013 | Maximilian P. L. Haslbeck | ** verified ** 复杂性理论条目 |
| 2016 | ... | 计算复杂性基础 |

### 5.4 其他参考

| 项目 | 语言 | 内容 | 链接 |
|------|------|------|------|
| Agda: Complexity Theory | Agda | 复杂度理论形式化尝试 | 社区项目 |
| HOL4: Complexity | HOL4 | 基础复杂度定义 | 社区项目 |

---

## 6. 建议的优先实现路径

### 路径 A: 直接扩展 Issue #35366 (推荐)

基于 KrystianYC 的已完成工作，逐步扩展：

```
Phase 1: 合并基础设施 (1-2 周)
├── PR 1: `step_none_iff` 到 `PostTuringMachine.lean`
├── PR 2: `runN` + 引理到 `TM1Complexity.lean`
└── PR 3: P/NP 类定义 + `p_sub_np` 定理

Phase 2: 扩展核心定义 (2-3 周)
├── NP-Hard 定义
├── NP-Complete 定义
├── 多项式时间归约 (≤ₚ)
└── 与 Simas 框架的对接

Phase 3: Cook-Levin 定理 (4-6 周)
├── SAT 形式化
├── TM 配置编码为布尔公式
├── 转移函数的正确性编码
├── 多项式大小界限证明
└── 最终归约构造

Phase 4: 应用与扩展 (2-4 周)
├── SAT 的 NP-完全性证明
├── 其他 NP-完全问题归约
└── TM1 ↔ TM2 多项式等价
```

### 路径 B: 新建独立项目 (风险更高)

新建 `lean-complexity` 或 `mathlib-complexity` 库：
- 优点: 不受 mathlib 审查流程约束
- 缺点: 与 mathlib 生态隔离，难以复用

### 路径 C: 移植 Isabelle AFP (工作量最大)

直接参考 Isabelle AFP 的 Cook-Levin 实现进行移植：
- 优点: 经过验证的完整路径
- 缺点: Isabelle→Lean 的概念映射工作量巨大

---

## 7. 关键技术决策点

### 决策 1: 基础 TM 模型选择

| 选项 | 优点 | 缺点 |
|------|------|------|
| **TM1 (现有)** | 已有大量引理；KrystianYC 已完成工作 | 非标准教科书模型 |
| **TM2 + FinTM2** | 更接近标准定义；有 `EvalsToInTime` | 与现有 P/NP 工作正交 |
| **BoltonBailey 的 FinTM0** | bundled 类型，更结构化 | 新建模型，需要大量引理重建 |
| **λ-演算 (Simas)** | 更易于程序验证 | 需要证明与 TM 等价 |

**建议**: 选择 **TM1 (Issue #35366 方案)**，因为它已完成且与现有 Mathlib 兼容。

### 决策 2: 时间计数风格

| 选项 | 优点 | 缺点 |
|------|------|------|
| **燃料型 `runN`** | 简单；单调性证明直接 | 信息量较少 |
| **结构型 `EvalsToInTime`** | 包含停机证明 | 更复杂 |

**建议**: 两种方案都可接受，社区应协调统一。建议支持**两种风格**的接口。

### 决策 3: 接受状态定义

| 选项 | 优点 | 缺点 |
|------|------|------|
| **磁带头部谓词** (KrystianYC) | 灵活；无需修改 TM 模型 | 非标准 |
| **显式接受/拒绝状态** | 教科书标准 | 需要扩展 TM 定义 |

**建议**: **磁带头部谓词**方案更 Lean-idiomatic，与 Mathlib 风格一致。

---

## 8. 社区讨论记录

### 8.1 Lean Zulip 相关讨论

| 时间 | 主题 | 关键人物 | 内容 |
|------|------|---------|------|
| 2021-11 | Turing machines & gigantic numbers | DayDun, Mario Carneiro | 讨论 TM0 用于 Busy Beaver；Carneiro 提供了 busy_beaver 定义 |
| 2021-11 | Post-Turing machine 模型 | Mario Carneiro | 解释了 TM0 是 Post 的变体，每步只做 move 或 write |
| 2024-2025 | Complexity theory in Lean | 社区 | 多次讨论复杂度理论形式化的可行性 |

**关键引用** (Carneiro, 2021):
> "The model being used is pretty standard, the Post-Turing machine, where at each state you either do a move or a write (Turing's original formulation did both in one step, so this is a more restrictive model)"

### 8.2 GitHub Issue/PR 讨论

**Issue #35366** 中维护者的关键问题:
1. 是否应在 `Turing.TM1` 还是等待 PR #33132 的 `FinTM0` 上构建？
2. `runN` (燃料型) 是否可接受，还是更倾向 `EvalsTo`-风格？
3. `IsPolynomial` 是否应放在独立文件？

**尚未收到维护者的正式回复** (截至 2026-02-15)。

---

## 9. 相关 Mathlib4 Issues/PRs

| 编号 | 标题 | 作者 | 状态 | 链接 |
|------|------|------|------|------|
| **#35366** | P/NP for TM1 | KrystianYC | 🟡 待审查 | https://github.com/leanprover-community/mathlib4/issues/35366 |
| **#33132** | Single-tape TM complexity | BoltonBailey | 🟡 草案 | https://github.com/leanprover-community/mathlib4/pull/33132 |
| #6091 | 100 new theorems to prove | 社区 | 🟢 活跃 | 包含 Cook's theorem (NP-completeness of SAT) |
| #??? | `TMComputable.lean` | 社区 | ✅ 已合并 | 多带 TM + `FinTM2` |

---

## 10. 外部独立项目

### 10.1 Lean 4 复杂度项目

| 项目 | 作者 | 内容 | 状态 |
|------|------|------|------|
| KrystianYC/cli-and-ai | KrystianYC | P/NP 类 + `p_sub_np` | 活跃，待合并 |
| Simas arXiv:2601.15571 | T. Simas | 多项式时间归约框架 | 已发布 |
| Witten-Helffer-Sjöstrand 项目 | 未知 | P=NP 与谱几何的不相容性 | 未知 |

### 10.2 其他 Proof Assistant

| 项目 | 证明助手 | 内容 | 年份 |
|------|---------|------|------|
| AFP Cook_Levin | Isabelle | 完整 Cook-Levin | 2025 |
| cook-levin (uds-psl) | Coq | 完整 Cook-Levin + P/NP | 2021 |
| 其他 | Coq/Isabelle | 基础复杂度定义 | 2013-2016 |

---

## 11. 对 Sylva Formalization 项目的建议

### 短期目标 (1-2 周)

1. **联系 KrystianYC** 获取 Issue #35366 的完整代码并测试编译
2. **审查代码质量**，评估是否可作为 mathlib PR 的基础
3. **协调 BoltonBailey** 的 PR #33132，确定两种方案的整合策略

### 中期目标 (2-4 周)

1. **提交 PR 1**: `step_none_iff` 和基础引理
2. **提交 PR 2**: `runN` + 复杂度基础设施
3. **提交 PR 3**: P/NP 类定义 + `p_sub_np`
4. **研究 Isabelle AFP** 的 SAT 编码策略

### 长期目标 (1-3 月)

1. **形式化 SAT** 在 Lean 4 中
2. **实现 TM→SAT 编码** (Cook-Levin 的核心)
3. **证明 SAT 是 NP-Complete**
4. **建立从 SAT 到其他问题的归约链**

### 关键依赖

```
mathlib4
├── PostTuringMachine.lean (TM0/TM1)        ✅ 已存在
├── TM1Complexity.lean (runN, InP, InNP)    🔄 待合并 (Issue #35366)
├── SAT.lean (可满足性)                    ❌ 缺失
├── TMEncoding.lean (配置编码)              ❌ 缺失
├── CookLevin.lean (主定理)                 ❌ 缺失
└── NPComplete.lean (NP-完全性)            ❌ 缺失
```

---

## 12. 参考文献与资源

### 12.1 Lean/Mathlib 资源

1. **Carneiro, M.** (2018). `PostTuringMachine.lean`. Mathlib3.  
   https://github.com/leanprover-community/mathlib/blob/master/src/computability/PostTuringMachine.lean

2. **KrystianYC.** (2026). "P/NP for TM1 — Issue #35366".  
   https://github.com/leanprover-community/mathlib4/issues/35366

3. **BoltonBailey.** (2025). "Single-tape TM complexity — PR #33132".  
   https://github.com/leanprover-community/mathlib4/pull/33132

4. **Simas, T.** (2026). "Computational Complexity of Physical Counting".  
   arXiv:2601.15571. https://arxiv.org/abs/2601.15571

### 12.2 外部形式化资源

5. **Weidenbach, C.** (2025). "Cook-Levin Theorem". Isabelle AFP.  
   https://devel.isa-afp.org/entries/Cook_Levin.html

6. **Gäher, L. & Kunze, F.** (2021). "Mechanising Complexity Theory: The Cook-Levin Theorem in Coq".  
   ITP 2021. https://doi.org/10.4230/LIPIcs.ITP.2021.20

7. **Gäher, L. & Kunze, F.** (2021). Code repository.  
   https://github.com/uds-psl/cook-levin

### 12.3 教科书参考

8. **Sipser, M.** (1996). *Introduction to the Theory of Computation*.  
   Chapter 7: Time Complexity; §3.1 for TM acceptance.

9. **Hopcroft, J.E., Motwani, R., & Ullman, J.D.** (2006).  
   *Introduction to Automata Theory, Languages, and Computation*.

10. **Korte, B. & Vygen, J.** (2012). *Combinatorial Optimization: Theory and Algorithms*.

---

## 13. 附录: 术语对照表

| 英文 | 中文 | Lean 符号 (待确定) |
|------|------|-------------------|
| Complexity Class | 复杂度类 | `ComplexityClass` |
| P (Polynomial Time) | 多项式时间 | `InP` |
| NP (Nondeterministic Polynomial) | 非确定性多项式时间 | `InNP` |
| NP-Complete | NP-完全 | `IsNPComplete` |
| NP-Hard | NP-难 | `IsNPHard` |
| Polynomial-time reduction | 多项式时间归约 | `PolynomialReduction` |
| Cook-Levin Theorem | Cook-Levin 定理 | `cook_levin` |
| SAT (Satisfiability) | 可满足性问题 | `SAT` |
| Turing Machine | 图灵机 | `Turing.TM1` |
| Verifier | 验证器 | `verifier` |
| Certificate | 证书/见证 | `certificate` |

---

*报告完成。最后更新: 2026-06-03*
