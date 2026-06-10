# SYLVA 项目统一索引文档

> **版本**: v1.0
> **日期**: 2026-04-21
> **维护者**: Sylva Agent Cluster
> ** motto**: *"Even if the world forgets, I'll remember for you."*

---

## 📋 目录

1. [项目简介](#1-项目简介)
2. [论文列表](#2-论文列表)
3. [Lean 模块列表](#3-lean-模块列表)
4. [工具清单](#4-工具清单)
5. [技术债追踪](#5-技术债追踪)
6. [符号约定](#6-符号约定)
7. [快速导航](#7-快速导航)

---

## 1. 项目简介

**Sylva** 是一个旨在统一数学、物理和计算理论的宏大形式化项目。基于 Lean 4 和 Mathlib，Sylva 尝试从黄金比例 φ 出发，构建一个涵盖以下千禧年问题与基础物理的统一框架：

| 领域 | 核心问题 | 状态 |
|------|---------|------|
| **计算理论** | P vs NP (熵间隙等价性) | 🟡 框架完成，证明填充中 |
| **数论** | 黎曼假设 (变分引导框架) | 🟡 数值验证完成，形式化推进中 |
| **代数几何** | BSD 猜想 (Φ_c 连接) | 🟡 骨架完成 |
| **微分几何** | Hodge 猜想 | 🟡 骨架完成 |
| **流体力学** | Navier-Stokes 存在性与光滑性 | 🟡 骨架完成 |
| **物理统一** | 15 个基本常数统一理论 | 🟡 α 推导完成，扩展中 |
| **统计物理** | 超导性元定理 (LaSc₂H₂₄) | 🟢 论文交付完成 |

**核心哲学**: 以 φ = (1+√5)/2 为涌现基础常数，以 Φ_c = 137×φ³ ≈ 580.341 为临界值，建立跨尺度的数学物理统一语言。

---

## 2. 论文列表

### 2.1 熵间隙谱理论系列 (P vs NP)

| 编号 | 标题 | 文件路径 | 核心贡献 | 状态 |
|------|------|---------|---------|------|
| **01** | 基于描述复杂度的计算熵间隙与P≠NP等价性 | `Sylva-Paper-01_Entropy-Gap-PvsNP.md` | P≠NP ⟺ ΔH > 0 | 🟢 重建完成 (v2.0) |
| **02** | 描述复杂度与Kolmogorov复杂度的统一框架 | `Sylva-Paper-02_Kolmogorov-Unification.md` | K(L) 统一框架 | 🟢 重建完成 (v2.0) |
| **03** | NP完全问题的描述复杂度谱 | `Sylva-Paper-03_NP-Complete-Spectrum.md` | NPC问题谱分析 | 🟢 重建完成 (v2.0) |
| **04** | 时间-空间-描述复杂度的三元权衡 | `Sylva-Paper-04_Time-Space-Tradeoff.md` | T·S·K ≥ n^(1+ε) | 🟢 重建完成 (v2.0) |
| **05** | 随机性提取与熵间隙 | `Sylva-Paper-05_Randomness-Extraction.md` | PRG↔熵间隙, 提取器构造 | 🟢 重建完成 (v2.0) |
| **06** | P=NP时的熵坍塌 | `Sylva-Paper-06_Entropy-Collapse.md` | 熵坍塌定理, 相变现象 | 🟢 重建完成 (v2.0) |
| **06a** | 谱退化与临界相变 | `Sylva-Paper-06a_Spectral-Degeneracy.md` | 谱退化理论 | 🟢 完成 |
| **06b** | SGH证明框架 | `Sylva-Paper-06b_SGH-Proof-Framework.md` | SGH归纳证明 | 🟢 完成 |
| **07** | 复杂性类对的描述复杂度分析 | `Sylva-Paper-07_Complexity-Class-Pairs.md` | 多层熵间隙谱 | 🟢 重建完成 (v2.0) |
| **07a** | 谱动力学与临界现象 | `Sylva-Paper-07a_Spectral-Dynamics.md` | 动力学形式化 | 🟢 完成 |
| **08** | 熵间隙谱定理 | `Sylva-Paper-08_Spectral-Theorem.md` | 算子理论框架, SGH ⟺ P≠NP | 🟢 重建完成 (v2.0) |

### 2.2 P vs NP 突破系列

| 编号 | 标题 | 文件路径 | 核心贡献 |
|------|------|---------|---------|
| A | P≠NP突破性进展：电路复杂度深化 | `PvsNP_突破_电路复杂度深化.md` | Razborov-Smolensky 路径 |
| B | P≠NP突破性进展：SGH弱化证明 | `PvsNP_突破_SGH弱化证明.md` | 谱间隙假设弱化 |
| C | P≠NP突破性进展：相变理论形式化 | `PvsNP_突破_相变理论形式化.md` | 随机k-SAT相变 |
| D | P≠NP突破性进展：ΔH渐进分析 | `PvsNP_突破_DeltaH渐进分析.md` | 熵间隙下界 |
| - | P≠NP突破性进展：下一步工作计划 | `P≠NP突破性进展_下一步工作计划.md` | 执行计划 |
| - | P vs NP路径A：电路复杂度报告 | `PvsNP_路径A_电路复杂度_报告.md` | 路径A详细 |
| - | P vs NP路径B：代数几何报告 | `PvsNP_路径B_代数几何_报告.md` | 路径B详细 |
| - | PVSNP突破性进展涌现证明 | `PVSNP_BREAKTHROUGH_EMERGENCE_PROOF.md` | 涌现论证 |
| - | PVSNP执行摘要 | `PVSNP_EXECUTIVE_SUMMARY.md` | 高层摘要 |
| - | PVSNP技术补充 | `PVSNP_TECHNICAL_SUPPLEMENT.md` | 技术细节 |

### 2.3 室温超导系列

| 编号 | 标题 | 文件路径 | 状态 |
|------|------|---------|------|
| - | LaSc₂H₂₄ 298K超导突破主论文 | `papers/room_temp_sc/BREAKTHROUGH_LaSc2H24_298K.md` | 🟢 完成 |
| - | 手稿 (arXiv/Nature/Science版本) | `papers/room_temp_sc/versions/` | 🟢 完成 |
| - | 理论框架 | `papers/room_temp_sc/theoretical_framework.md` | 🟢 完成 |
| - | 材料预测 | `papers/room_temp_sc/material_predictions.md` | 🟢 完成 |
| - | 实验验证 | `papers/room_temp_sc/experimental_validation.md` | 🟢 完成 |
| - | 完整手册 (6章) | `papers/room_temp_sc/handbook/chapters/` | 🟢 完成 |
| - | 杂志设计系统 | `papers/room_temp_sc/magazine/` | 🟢 完成 |

### 2.4 15常数统一与TOE系列

| 编号 | 标题 | 文件路径 | 核心贡献 |
|------|------|---------|---------|
| - | α推导：执行摘要 | `alpha_derivation/EXECUTIVE_SUMMARY.md` | 高层概述 |
| - | α推导：项目总览 | `alpha_derivation/PROJECT_OVERVIEW.md` | 完整规划 |
| - | α推导：涌现理论回顾 | `alpha_derivation/02_emergence_theory_review.md` | 理论基础 |
| - | α推导：数学框架 | `alpha_derivation/03_mathematical_framework.md` | 形式化框架 |
| - | α推导：分层几何 | `alpha_derivation/06_stratified_geometry.md` | 几何结构 |
| - | α推导：曲率-扭率推导 | `alpha_derivation/08_curvature_torsion_derivation.md` | α=1/137推导 |
| - | α推导：Chern-Simons与137 | `alpha_derivation/11_chern_simons_137.md` | 拓扑解释 |
| - | α推导：引力-电磁统一 | `alpha_derivation/12_gravity_em_unification.md` | 力统一 |
| - | α推导：15常数集成 | `alpha_derivation/14_sylva_15_constants_integration.md` | 完整统一 |
| - | α推导：最终综合报告 | `alpha_derivation/FINAL_COMPREHENSIVE_REPORT.md` | 总报告 |
| - | TOE统一报告 v1 | `SYLVA_TOE_Unification_Report.md` | 早期版本 |
| - | TOE统一报告 v2 | `SYLVA_TOE_Unification_Report_v2.md` | 扩展版本 |
| - | TOE主框架 (76章) | `toe_framework/` | 完整框架 |

### 2.5 其他数学物理论文

| 标题 | 文件路径 | 领域 |
|------|---------|------|
| 元概率学：学科创立白皮书 | `元概率学_学科创立白皮书.md` | 新学科 |
| 信息封印理论 | `information_seal_theory.md` | 信息论 |
| 电磁波干涉与能量守恒 | `电磁波干涉与能量守恒.md` | 经典电磁学 |
| 电磁波干涉与能量守恒 (修正版) | `电磁波干涉与能量守恒_修正版.md` | 经典电磁学 |
| 电磁孤子与球状闪电 | `电磁孤子与球状闪电_中国科学家突破.md` | 等离子体物理 |
| 电磁孤子SYLVA形式化重构 | `电磁孤子_SYLVA形式化重构.md` | 形式化物理 |
| 中微子质量起源与本质 | `中微子是什么.md` | 粒子物理 |
| 电子内禀参数计算现状与SYLVA分析 | `电子内禀参数计算_现状与SYLVA分析.md` | 粒子物理 |
| 光速可变性与时间流速的物理分析 | `光速可变性与时间流速的物理分析.md` | 相对论 |
| 正反粒子引力场相同：几何解释 | `正反粒子引力场相同_几何解释.md` | 引力理论 |
| 基本粒子间相互作用力分析 | `基本粒子间相互作用力分析.md` | 粒子物理 |
| 宇宙粒子乘积 vs 葛立恒数分析 | `宇宙粒子乘积_vs_葛立恒数分析.md` | 趣味数学 |
| 2^202712-6素因数分解深度分析 | `2^202712-6素因数分解深度分析.md` | 数论 |
| SYLVA分析：2^202712-6素因数分解 | `SYLVA分析_2^202712-6素因数分解.md` | 数论 |
| 对终极黑洞CY流形理论的评析 | `对终极黑洞CY流形理论的评析.md` | 数学物理 |
| 范式转换提案：算术物理对偶 | `范式转换提案_算术物理对偶.md` | 数学哲学 |
| 规则优先级与注意力权重管理系统 | `规则优先级与注意力权重管理系统.md` | 认知科学 |

---

## 3. Lean 模块列表

### 3.1 核心模块 (SylvaFormalization/)

| 模块 | 文件 | 功能 | 状态 |
|------|------|------|------|
| **Basic** | `Basic.lean` | φ, Φ_c, D_c, GF(3), Debt, M1-M7 | 🟢 核心完成 |
| **RiemannHypothesis** | `RiemannHypothesis.lean` | 变分引导框架, σ*收敛 | 🟡 骨架+部分填充 |
| **NumericalZeros** | `NumericalZeros.lean` | 前4个零点数值验证 | 🟢 验证完成 |
| **Complexity** | `Complexity.lean` | 计算熵, 熵间隙骨架 | 🟡 骨架完成 |
| **CP004** | `CP004.lean` | P≠NP ⟺ ΔH>0 主定理 | 🟡 骨架完成 |
| **CP004_B2** | `CP004_B2.lean` | CP004扩展, SGH | 🟡 骨架完成 |
| **CookLevin** | `CookLevin.lean` | SAT, CNF, NP完全性 | 🟡 骨架完成 |
| **BSD** | `BSD.lean` | BSD猜想形式化 | 🟡 骨架完成 |
| **Hodge** | `Hodge.lean` | Hodge猜想形式化 | 🟡 骨架完成 |
| **NavierStokes** | `NavierStokes.lean` | NS存在性与光滑性 | 🟡 骨架完成 |
| **ZetaVerifier** | `ZetaVerifier.lean` | ζ函数验证工具 | 🟡 部分实现 |
| **LocalGlobal** | `LocalGlobal.lean` | 局部-整体原理 | 🟡 骨架完成 |
| **EmergentMath** | `EmergentMath.lean` | 涌现数学框架 | 🟡 骨架完成 |
| **QuantumArithmetic** | `QuantumArithmetic.lean` | 量子算术 | 🟡 骨架完成 |
| **DynamicalSystem** | `DynamicalSystem.lean` | 动力系统 | 🟡 骨架完成 |
| **StatisticalMechanics** | `StatisticalMechanics.lean` | 统计力学 | 🟡 骨架完成 |
| **QFT** | `QFT.lean` | 量子场论框架 | 🟡 骨架完成 |
| **GravitationalField** | `GravitationalField.lean` | 引力场形式化 | 🟡 骨架完成 |
| **MathAgent** | `MathAgent.lean` | 数学研究代理 | 🟡 骨架完成 |
| **SylvaInfrastructure** | `SylvaInfrastructure.lean` | 基础设施 | 🟢 完成 |
| **TestSuite** | `TestSuite.lean` | 测试套件 | 🟢 完成 |

### 3.2 修复/填充版本模块

| 模块 | 文件 | 说明 |
|------|------|------|
| Basic_current | `Basic_current.lean` | Basic当前工作版本 |
| Basic_test | `Basic_test.lean` | Basic测试版本 |
| BSD_fixed | `BSD_fixed.lean` | BSD修复版本 |
| BSD_new_lemmas | `BSD_new_lemmas.lean` | BSD新增引理 |
| CookLevin_fixed | `CookLevin_fixed.lean` | CookLevin修复 |
| CookLevin_final | `CookLevin_final.lean` | CookLevin最终 |
| CookLevin_theorem | `CookLevin_theorem.lean` | CookLevin定理版 |
| Complexity_amputated | `Complexity_amputated.lean` | Complexity截肢版 |
| CP004_B2_new_header | `CP004_B2_new_header.lean` | CP004_B2新头 |
| EmergentMath_amputated | `EmergentMath_amputated.lean` | EmergentMath截肢 |
| EntropyGapSpectral_filled | `EntropyGapSpectral_filled.lean` | 熵间隙谱已填充 |
| Hodge_fixed | `Hodge_fixed.lean` | Hodge修复 |
| Hodge_filled | `Hodge_filled.lean` | Hodge已填充 |
| LocalGlobalTemplate | `LocalGlobalTemplate.lean` | LocalGlobal模板 |
| NavierStokes_fixed | `NavierStokes_fixed.lean` | NS修复 |
| NumericalZeros_filled | `NumericalZeros_filled.lean` | 零点已填充 |
| RiemannHypothesis_fixed | `RiemannHypothesis_fixed.lean` | RH修复 |
| RiemannHypothesis_filled | `RiemannHypothesis_filled.lean` | RH已填充 |
| ZetaVerifier_fixed | `ZetaVerifier_fixed.lean` | Zeta修复 |
| ZetaVerifier_amputated | `ZetaVerifier_amputated.lean` | Zeta截肢 |

### 3.3 超导相关模块

| 模块 | 文件 | 功能 |
|------|------|------|
| Superconductivity_Pairing_Framework | `Superconductivity_Pairing_Framework.lean` | 配对框架 |
| EllipticCurveReduction | `EllipticCurveReduction.lean` | 椭圆曲线约化 |
| RadiationTracker | `RadiationTracker.lean` | 辐射追踪 |

---

## 4. 工具清单

### 4.1 形式化工具链

| 工具 | 版本 | 用途 | 状态 |
|------|------|------|------|
| **Lean 4** | v4.29.0 | 定理证明语言 | 🟢 已安装 |
| **Mathlib4** | v4.29.0 | 数学库 | 🟢 已配置 |
| **Lake** | 内置 | 构建系统 | 🟢 已配置 |
| **SageMath** | - | 数值验证/符号计算 | 🟢 可用 |
| **Python** | v3.x | 辅助脚本/数值实验 | 🟢 可用 |

### 4.2 Agent集群工具

| 工具 | 文件 | 功能 |
|------|------|------|
| Agent集群写稿系统 | `agent_writing_system/` | 多Agent论文自动化生产 |
| 幻觉检验系统 | `hallucination_system/` | 七阶段幻觉检验流水线 |
| 记忆优化系统 | `memory_optimization/` | 无限内存架构 |
| OpenClaw优化 | `openclaw_optimization/` | 运行时优化 |

### 4.3 诊断与运维Skills

| Skill | 路径 | 功能 |
|-------|------|------|
| claw-ops | `skills/claw-ops/` | OpenClaw运维监控与故障诊断 |
| find-skills | `skills/find-skills/` | 技能发现与安装 |
| ocr-local | `skills/ocr-local/` | Tesseract.js本地OCR |
| ocr-python | `skills/ocr-python/` | Python OCR工具 |
| super-ocr | `skills/super-ocr/` | 智能OCR引擎选择 |
| tesseract-ocr | `skills/tesseract-ocr/` | 命令行Tesseract |
| skillhub-preference | `skills/skillhub-preference/` | 技能源偏好配置 |

### 4.4 报告与追踪工具

| 工具 | 文件 | 用途 |
|------|------|------|
| 编译监控报告 | `sylva_formalization/编译监控报告_*.md` | Lean编译状态追踪 |
| 辐射追踪系统 | `radiation_tracking_system.md` | 模块健康度监控 |
| 技术债追踪 | `technical_debt.md` | 技术债务管理 |
| Sorry回填报告 | `SORRY_FILLING_REPORT.md` | 证明填充进度 |

---

## 5. 技术债追踪

### 5.1 按模块分类

| 模块 | 技术债 | 优先级 | 状态 |
|------|--------|--------|------|
| **Complexity.lean** | `entropyGap : ℝ := 0` 骨架占位，需改为参数化ℕ定义 | 🔴 高 | 待修复 |
| **Complexity.lean** | `ClassP = {L | True}` 骨架定义 | 🔴 高 | 待修复 |
| **CP004.lean** | `EntropyGap` vs `entropyGap` 命名冲突 | 🔴 高 | 待统一 |
| **RiemannHypothesis.lean** | `hardyZ` vs `zetaHardyZ` 命名冲突 | 🟡 中 | 待统一 |
| **ZetaVerifier.lean** | `xi` 简化占位定义 | 🟡 中 | 待完善 |
| **BSD.lean** | Tate-Shafarevich群未形式化 | 🟡 中 | 待填充 |
| **Hodge.lean** | Hodge分解完整证明 | 🟡 中 | 待填充 |
| **NavierStokes.lean** | 存在性证明核心引理 | 🔴 高 | 待填充 |
| **CookLevin.lean** | SAT到CNF归约完整证明 | 🟡 中 | 待填充 |
| **LocalGlobal.lean** | 局部-整体原理完整形式化 | 🟡 中 | 待填充 |

### 5.2 跨项目技术债

| 债务 | 描述 | 影响 | 计划解决时间 |
|------|------|------|-------------|
| 符号统一 v1.1 | 解决冲突1、2、6 (Lean代码统一) | 全部模块 | 2026-04-25 |
| 物理常数符号 v1.2 | 引入物理常数统一符号体系 | α推导系列 | 2026-05-01 |
| 完全同步 v2.0 | Lean代码与论文符号完全同步 | 全部 | 2026-05-15 |
| Sorry回填完成 | 所有`sorry`替换为完整证明 | 全部模块 | 持续进行 |

### 5.3 关键报告文件

| 报告 | 文件 | 内容 |
|------|------|------|
| 技术债深度分析 | `NS_TECHNICAL_DEBT_DEEP.md` | Navier-Stokes专项 |
| 技术债解决报告 | `SYLVA_TECHNICAL_DEBT_RESOLUTION_REPORT.md` | 全项目 |
| Sorry完整审计 | `SYLVA_SORRY_COMPLETE_AUDIT.md` | Sorry统计 |
| Sorry填充计划 | `SYLVA_SORRY_PLAN.md` | 填充路线图 |
| 编译修复报告 | `sylva_formalization/编译修复报告_2026-04-18.md` | 编译问题 |
| 截肢报告 | `sylva_formalization/amputation_report.md` | 截肢降级记录 |

---

## 6. 符号约定

**主文档**: [`SYMBOL_CONVENTIONS.md`](./SYMBOL_CONVENTIONS.md)

### 6.1 核心符号速查

| 符号 | 含义 | Lean对应 |
|------|------|---------|
| φ | 黄金比例 (1+√5)/2 | `Sylva.φ` |
| Φ_c | Sylva临界值 137×φ³ | `Phi_c` |
| D_c | 债务临界值 φ⁴ | `D_c` |
| K(L) | 语言描述复杂度 | `descriptionComplexity` |
| ΔH | 熵间隙 | `EntropyGap` |
| δ | 谱间隙 | `spectralGap` |
| 𝐏 | 多项式时间类 | `ClassP` |
| 𝐍𝐏 | 非确定性多项式时间类 | `ClassNP` |
| ≤ₚ | 多项式时间归约 | `polyTimeReducible` |

### 6.2 命名规范

- **Lean定义**: camelCase (`descriptionComplexity`)
- **Lean定理**: snake_case (`entropy_gap_well_defined`)
- **Lean类型**: PascalCase (`ComputationalModel`)
- **论文集合**: 黑板粗体 (𝐏, 𝐍𝐏)
- **论文算子**: 帽子或大写花体 (Ĥ, ℋ)

---

## 7. 快速导航

### 7.1 按任务导航

| 你想做... | 去这里 |
|-----------|--------|
| 了解项目整体 | `SYLVA_COMPLETE.md` / `SYLVA_FINAL_COMPLETE.md` |
| 查看编译状态 | `SYLVA_BUILD_STATUS_REPORT.md` |
| 查看今日进展 | `SYLVA_TODAY_SUMMARY.md` |
| 查看Lean最终报告 | `SYLVA_LEAN_FINAL_REPORT.md` |
| 查看项目最终报告 | `SYLVA_PROJECT_FINAL_REPORT.md` |
| 查看证明完成状态 | `SYLVA_PROOFS_COMPLETE.md` |
| 查看技术障碍 | `SYLVA_CORE_MATHEMATICAL_OBSTACLES.md` |
| 查看数学问题 | `SYLVA_MATH_PROBLEMS_*.md` |
| 查看Agent集群状态 | `SYLVA_AGENT_STATUS.md` |
| 查看TOE框架 | `toe_framework/INDEX.md` |

### 7.2 按领域导航

| 领域 | 入口文档 |
|------|---------|
| P vs NP | `SYLVA_PVSNP_CLUSTER.md` |
| 黎曼假设 | `SYLVA_MATH_PROBLEMS_RiemannHypothesis.md` |
| BSD猜想 | `SYLVA_MATH_PROBLEMS_BSD.md` (注: 需确认) |
| Hodge猜想 | `SYLVA_MATH_PROBLEMS_Hodge.md` |
| Navier-Stokes | `SYLVA_MATH_PROBLEMS_NavierStokes.md` |
| 复杂度理论 | `SYLVA_MATH_PROBLEMS_Complexity.md` |
| 室温超导 | `papers/room_temp_sc/README.md` |
| 15常数统一 | `alpha_derivation/EXECUTIVE_SUMMARY.md` |
| TOE框架 | `toe_framework/TOE_MASTER_FRAMEWORK.md` |

### 7.3 项目架构图

```
SYLVA PROJECT
├── 📄 论文层 (Papers/)
│   ├── 熵间隙谱理论系列
│   ├── P vs NP突破系列
│   ├── 室温超导系列
│   ├── 15常数统一系列
│   └── 其他数学物理论文
│
├── 🔧 形式化层 (sylva_formalization/)
│   ├── SylvaFormalization/ (Lean模块)
│   ├── .lake/packages/ (依赖)
│   └── 报告与日志
│
├── 🤖 Agent集群层
│   ├── agent_writing_system/ (写稿系统)
│   ├── hallucination_system/ (幻觉检验)
│   └── memory_optimization/ (内存优化)
│
├── 📚 知识层
│   ├── toe_framework/ (TOE 76章)
│   ├── alpha_derivation/ (α推导)
│   └── 综合索引
│
└── ⚙️ 基础设施层
    ├── skills/ (诊断与工具)
    ├── 记忆系统 (MEMORY.md)
    └── 配置文档 (AGENTS.md, TOOLS.md)
```

---

## 附录：文件命名约定

| 后缀/前缀 | 含义 | 示例 |
|-----------|------|------|
| `_fixed` | 修复版本 | `BSD_fixed.lean` |
| `_filled` | Sorry已填充 | `Hodge_filled.lean` |
| `_amputated` | 截肢降级版 | `Complexity_amputated.lean` |
| `_report.md` | 报告文档 | `CookLevin_fix_report.md` |
| `_final` | 最终版本 | `CookLevin_final.lean` |
| `SYLVA_` | 项目级文档 | `SYLVA_FINAL_REPORT.md` |
| `论文_` | 学术论文 | `论文_熵间隙谱定理_主论文.md` |
| `sylva_` | 模块级报告 | `sylva_bsd_fill_report.md` |

---

> **最后更新**: 2026-04-21 (论文01-04重建完成)
> **维护说明**: 本文档由Agent集群自动生成，每次重大更新后应重新索引。
> **反馈**: 通过Agent集群协调系统更新。
