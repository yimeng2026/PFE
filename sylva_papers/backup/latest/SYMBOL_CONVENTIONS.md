# Sylva 数学符号约定文档
# Sylva Mathematical Symbol Conventions

**版本**: v1.0  
**日期**: 2026-04-21  
**适用范围**: Sylva形式化项目全部论文与Lean代码  
**维护原则**: 本文档为单一事实来源（Single Source of Truth），所有论文和代码必须遵循

---

## 1. 核心符号速查表

| 符号 | 含义 | 首次定义 | 使用位置 |
|------|------|---------|---------|
| $K(L)$ / `descriptionComplexity` | 语言 $L$ 的描述复杂度 | 论文A 定义2.11 | 全部论文、CP004.lean |
| $\Delta H$ / `entropyGap` | 熵间隙 | 论文A 第1.1节 | 全部论文、CP004.lean |
| $\hat{H}$ / `descriptionComplexityHamiltonian` | 描述复杂度哈密顿算子 | 论文A 定义2.12 | 论文A、B |
| $\delta$ / `spectralGap` | 谱间隙 | 论文A 定义5.1 | 论文A、B、SGH系列 |
| $\lambda_k$ | 第 $k$ 个特征值（能级） | 论文A 定理4.1 | 论文A、B |
| $\varphi$ / `φ` | 黄金比例 $(1+\sqrt{5})/2$ | Basic.lean | 全部Lean代码、α推导 |
| $\Phi_c$ / `Phi_c` | Sylva临界值 $137 \times \varphi^3$ | Basic.lean | Basic.lean、α推导 |
| $D_c$ / `D_c` | 债务临界值 $\varphi^4$ | Basic.lean | Basic.lean |
| $\Lambda(5/2)$ / `Lambda` | 临界分形维度算子 | Basic.lean | Basic.lean |
| $\mathbf{P}$ / `ClassP` | 多项式时间复杂性类 | 论文A 第1.1节 | 全部论文、Complexity.lean |
| $\mathbf{NP}$ / `ClassNP` | 非确定性多项式时间类 | 论文A 第1.1节 | 全部论文、Complexity.lean |
| SGH | 谱间隙假设 | 论文A 定义5.1 | 论文A、B、SGH系列 |
| SSGH | 强谱间隙假设 | 论文A 猜想5.4 | 论文A、B |

---

## 2. 按领域分类的符号定义

### 2.1 描述复杂度与熵理论

#### 2.1.1 字符串级复杂度

| 符号 | 数学定义 | Lean对应 | 备注 |
|------|---------|---------|------|
| $K(x)$ | 字符串 $x$ 的Kolmogorov复杂度 | `KolmogorovComplexity` | 论文D 第2.1节 |
| $K(x \mid y)$ | 条件Kolmogorov复杂度 | — | 论文D 第2.1节 |
| $C_{LZ78}(x)$ | LZ78归一化复杂度 | — | 论文D 第2.2.2节 |

#### 2.1.2 语言级描述复杂度

| 符号 | 数学定义 | Lean对应 | 备注 |
|------|---------|---------|------|
| $K(L)$ | $\min\{\|\langle M \rangle\| : M \text{ 判定 } L\}$ | `descriptionComplexity` | **核心符号** |
| $K(L^{(n)})$ | 长度 $n$ 截断的描述复杂度 | — | 论文A 定义2.11 |
| $K(L_n)$ | $L_n = L \cap \{0,1\}^n$ | — | 论文A 定义2.3 |
| $\overline{K}(L)$ | 平均描述复杂度 | — | 论文A 第2.3节 |
| $K_{\max}(L, n)$ | $\sup_{|x|=n} K(x \mid L)$ | `DescriptionComplexityMax` | Complexity.lean (骨架) |
| $K_{\min}(L, n)$ | $\inf_{|x|=n} K(x \mid L)$ | `DescriptionComplexityMin` | Complexity.lean (骨架) |

#### 2.1.3 熵与熵间隙

| 符号 | 数学定义 | Lean对应 | 备注 |
|------|---------|---------|------|
| $\Delta H$ | $\inf_{L \in \mathbf{NP}} K(L) - \sup_{L' \in \mathbf{P}} K(L')$ | `entropyGap` / `EntropyGap` | **核心符号** |
| $\Delta H(n)$ | 规模 $n$ 的熵间隙函数 | — | PvsNP_突破_DeltaH渐进分析.md |
| $\Delta H(V)$ | 代数簇 $V$ 的熵间隙 | — | 论文C 定义3.1 |
| $\Delta S(n, \alpha)$ | 参数 $\alpha$ 下的熵间隙 | — | 相变理论形式化 |
| $H_{\text{comp}}$ | 计算熵 | `ComputationalEntropy` | Complexity.lean |
| $H_{\text{Shannon}}$ | 香农熵 | — | 论文D 第1.1节 |

**冲突与解决方案**:
- **冲突1**: `entropyGap` (Complexity.lean) vs `EntropyGap` (CP004.lean) vs `entropyGap'` (CP004.lean)
  - **解决方案**: 统一使用 `EntropyGap`（大写E）作为规范名称，表示P vs NP的专用熵间隙。`entropyGap'` 作为通用两集合间熵间隙的辅助函数保留。
- **冲突2**: Complexity.lean 中 `entropyGap : ℝ := 0` 为全局常数，与 CP004 中参数化定义冲突
  - **解决方案**: Complexity.lean 中的定义是骨架占位，应以 CP004.lean 中的参数化定义 `EntropyGap (TM : Type) [ComputationalModel TM] : ℕ` 为准

---

### 2.2 算子与谱理论

#### 2.2.1 描述复杂度算子

| 符号 | 数学定义 | Lean对应 | 备注 |
|------|---------|---------|------|
| $\hat{H}$ | 描述复杂度哈密顿量 | — | 论文A 定义2.12 |
| $\mathcal{H}$ | 同 $\hat{H}$（论文B记号） | — | 论文B |
| $\mathcal{D}(\hat{H})$ | $\hat{H}$ 的定义域 | — | 论文A 定义2.12 |
| $\hat{H}_N$ | 截断算子（有限秩逼近） | — | 论文A 定理3.5 |
| $\hat{H}_{\text{sym}}$ | 对称化算子 | — | 论文A 修正定义3.2 |

**冲突与解决方案**:
- **冲突3**: 论文A 使用 $\hat{H}$，论文B 使用 $\mathcal{H}$
  - **解决方案**: 统一使用 $\hat{H}$ 作为规范符号，$\mathcal{H}$ 仅在需要区分不同算子变体时使用（如 $\mathcal{H}_{\text{eff}}$ 有效哈密顿量）

#### 2.2.2 谱与特征值

| 符号 | 数学定义 | Lean对应 | 备注 |
|------|---------|---------|------|
| $\sigma(\hat{H})$ | 算子 $\hat{H}$ 的谱 | — | 论文A 定理4.1 |
| $\lambda_k$ | 第 $k$ 个特征值 | — | 论文A 定理4.1 |
| $\lambda_0$ | 基态特征值 | — | 对应 $\mathbf{P}$ |
| $\lambda_1$ | 第一激发态 | — | 对应 $\mathbf{NP}$ |
| $\delta$ | 谱间隙 $\lambda_1 - \lambda_0$ | — | **核心符号** |
| $\delta(n)$ | 规模 $n$ 的谱间隙 | — | SGH系列 |
| $E_k$ | 第 $k$ 个特征空间 | — | 论文A 定理4.3 |
| $|\psi_k\rangle$ | 第 $k$ 个本征态 | — | 论文B 定义2.2 |
| $\mu_L$ | 谱测度 | — | 论文A 定义4.4 |

**冲突与解决方案**:
- **冲突4**: $\delta$ 在论文A中用于谱间隙，在BSD论文中可能用于其他含义
  - **解决方案**: 谱间隙统一使用 $\delta$ 或 $\Delta\lambda$，其他上下文使用下标区分（如 $\delta_{\text{BSD}}$）
- **冲突5**: $\lambda$ 在谱理论中用于特征值，在扩展图中用于扩展参数
  - **解决方案**: 扩展图参数改用 $\lambda_{\text{exp}}$ 或 $\varepsilon$

---

### 2.3 复杂性类

| 符号 | 含义 | Lean对应 | 备注 |
|------|------|---------|------|
| $\mathbf{P}$ | 多项式时间类 | `ClassP` | **核心符号** |
| $\mathbf{NP}$ | 非确定性多项式时间类 | `ClassNP` | **核心符号** |
| $\mathbf{PSPACE}$ | 多项式空间类 | — | 论文B 定理5.1 |
| $\mathbf{EXP}$ | 指数时间类 | — | 论文B 定理5.1 |
| $\mathbf{PH}$ | 多项式层次 | — | 论文B 推论4.5 |
| $\Sigma_k^{\mathbf{P}}$ | PH的第 $k$ 层 | — | 论文B 定理5.1 |
| $\mathbf{BQP}$ | 量子多项式时间类 | — | 论文A 问题7.5 |
| $\mathbf{AC}^0$ | 无界深度常数规模电路类 | — | Razborov-Smolensky |
| $\mathbf{P}/\mathbf{poly}$ | 非均匀多项式时间 | — | SGH弱化证明 |

**冲突与解决方案**:
- **冲突6**: Lean代码中 `ClassP` / `ClassNP` 定义为 `{L | True}`（骨架），与数学定义不一致
  - **解决方案**: 代码注释中必须标明当前为骨架实现，数学定义以本文档为准。未来填充时应使用正确的图灵机判定定义。

---

### 2.4 归约与多项式时间

| 符号 | 含义 | Lean对应 | 备注 |
|------|------|---------|------|
| $\leq_p$ | 多项式时间归约 | `≤ₚ` / `PolyTimeReducible` | **核心符号** |
| $\leq_m$ | 多一归约 | — | 标准记号 |
| $\leq_T$ | 图灵归约 | — | 标准记号 |
| $\text{TIME}(t(n))$ | 时间 $t(n)$ 复杂性类 | — | 时间层级定理 |

---

### 2.5 Sylva 基础常数

| 符号 | 数值/定义 | Lean对应 | 备注 |
|------|----------|---------|------|
| $\varphi$ | $(1+\sqrt{5})/2 \approx 1.618$ | `φ` / `Sylva.φ` | 黄金比例 |
| $\Phi_c$ | $137 \times \varphi^3 \approx 580.341$ | `Phi_c` | Sylva临界值 |
| $D_c$ | $\varphi^4 = 3\varphi + 2 \approx 6.854$ | `D_c` | 债务临界值 |
| $\lambda_c$ | $5/2 = 2.5$ | `lambda_c` | 临界阈值 |
| $\Lambda(x)$ | $x^{5/2}$ | `Lambda` | 分形维度算子 |
| $\Lambda_\varphi$ | $\varphi^{5/2}$ | `Lambda_phi` | — |

---

### 2.6 黎曼假设相关

| 符号 | 含义 | Lean对应 | 备注 |
|------|------|---------|------|
| $\zeta(s)$ | 黎曼ζ函数 | `zeta` | RiemannHypothesis.lean |
| $\xi(s)$ | 黎曼Xi函数 | `xi` | ZetaVerifier.lean |
| $Z(t)$ | Hardy Z函数 | `hardyZ` / `zetaHardyZ` | **冲突见下** |
| $\gamma_k$ | 第 $k$ 个非平凡零点虚部 | `ZETA_ZERO_k` | NumericalZeros.lean |
| $\theta(t)$ | Riemann-Siegel theta函数 | `riemannSiegelTheta` | NumericalZeros.lean |
| $\sigma$ | $\Re(s)$ | `s.re` | 复数实部 |
| $t$ | $\Im(s)$ | `s.im` | 复数虚部 |
| $\sigma^*$ | 最小化 $\sigma$ | `sigma_star` | RiemannHypothesis.lean |

**冲突与解决方案**:
- **冲突7**: `hardyZ` (RiemannHypothesis.lean) vs `zetaHardyZ` (ZetaVerifier.lean)
  - **解决方案**: 统一使用 `zetaHardyZ` 作为规范名称，`hardyZ` 作为别名保留但标记为弃用
- **冲突8**: `xi` 在 ZetaVerifier.lean 中为简化占位定义，与完整数学定义不一致
  - **解决方案**: 代码注释标明为简化版本，数学定义以标准黎曼Xi函数为准

---

### 2.7 代数几何（BSD / Hodge）

| 符号 | 含义 | Lean对应 | 备注 |
|------|------|---------|------|
| $E$ | 椭圆曲线 | `ShortWeierstrassCurve` | BSD.lean |
| $\Delta(E)$ | 判别式 | `discriminant` | BSD.lean |
| $\text{rank}(E)$ | 代数秩 | `rank_EllipticCurve` | BSD.lean |
| $L(E, s)$ | L函数 | `LFunction` | BSD.lean |
| $\text{Sha}$ / $\text{Ш}$ | Tate-Shafarevich群 | — | BSD.lean (注释) |
| $H^{p,q}$ | Hodge分解分量 | `hodgeDecomp` | Hodge.lean |
| $V$ | 代数簇 | — | 论文C |
| $\deg(V)$ | 簇的次数 | — | 论文C 定理2.4 |
| $H_V(t)$ | Hilbert多项式 | — | 论文C 定理2.4 |

---

### 2.8 物理常数统一理论

| 符号 | 含义 | 备注 |
|------|------|------|
| $\alpha$ | 精细结构常数 $1/137.036$ | 耦合型常数 |
| $\alpha_w$ | 弱耦合常数 $\approx 1/30$ | 耦合型常数 |
| $\alpha_s$ | 强耦合常数 | 耦合型常数 |
| $\alpha(d)$ | $d$ 维精细结构常数 | 论文03 定理3.2.1 |
| $m_e, m_\mu, m_\tau$ | 轻子质量 | 质量型常数 |
| $m_u, m_d, m_c, m_s, m_t, m_b$ | 夸克质量 | 质量型常数 |
| $m_h$ | 希格斯玻色子质量 | 质量型常数 |
| $v$ | 希格斯场vev | 质量型常数 |
| $\theta_{QCD}$ | QCD真空角 | 耦合型常数 |
| $\Omega_d$ | $d$ 维单位球面面积 | 论文03 定义3.1.1 |
| $\ell_P$ | 普朗克长度 | 论文03 |

---

### 2.9 相变理论

| 符号 | 含义 | 备注 |
|------|------|------|
| $\alpha$ | CNF子句-变量比 | 论文D 第4.1.1节 |
| $\alpha_c$ | 相变临界点 | 论文D 第4.2.1节 |
| $\nu$ | 临界指数 $\approx 1.5$ | 论文D 第4.2.1节 |
| $\beta$ | 标度指数 $\approx 0.5$ | 论文D 第4.2.2节 |
| $F_k(n, m)$ | 随机k-CNF公式 | 论文D 第4.1.1节 |
| $\mathcal{K}(\alpha)$ | 归一化描述复杂度极限 | 相变理论形式化 |

---

## 3. 命名约定

### 3.1 Lean代码命名规范

| 类别 | 规范 | 示例 |
|------|------|------|
| 定义/函数 | camelCase | `descriptionComplexity`, `computationalEntropy` |
| 定理/引理 | snake_case | `entropy_gap_well_defined`, `pneqnp_implies_positive_entropy_gap` |
| 类型/结构 | PascalCase | `ComputationalModel`, `BooleanCircuit` |
| 常数 | PascalCase或希腊字母 | `Phi_c`, `D_c`, `ZETA_ZERO_1` |
| 命名空间 | PascalCase | `Sylva`, `CP004`, `PvsNP` |
| 中缀运算符 | Unicode | `≤ₚ` (polyTimeReducible) |

### 3.2 论文LaTeX命名规范

| 类别 | 规范 | 示例 |
|------|------|------|
| 集合/空间 | 黑板粗体或花体 | $\mathbf{P}$, $\mathcal{L}$, $\mathbb{P}^n$ |
| 算子 | 帽子或大写花体 | $\hat{H}$, $\mathcal{H}$ |
| 复杂度函数 | 大写K | $K(L)$, $K(x)$ |
| 熵/间隙 | 大写希腊字母 | $\Delta H$, $\Delta S$ |
| 特征值 | 小写lambda | $\lambda_k$ |
| 谱间隙 | 小写delta | $\delta$ |
| 物理常数 | 小写希腊字母 | $\alpha$, $\varphi$ |
| Sylva专用常数 | 大写Phi/D + 下标c | $\Phi_c$, $D_c$ |

---

## 4. 冲突符号汇总与解决方案

| 编号 | 冲突符号 | 冲突上下文 | 解决方案 | 优先级 |
|------|---------|-----------|---------|--------|
| 1 | `entropyGap` vs `EntropyGap` | Complexity.lean vs CP004.lean | 统一使用 `EntropyGap`（大写E）作为P vs NP专用熵间隙 | 高 |
| 2 | `entropyGap : ℝ` vs `EntropyGap : ℕ` | 骨架vs完整实现 | 以CP004.lean中的参数化ℕ定义为准 | 高 |
| 3 | $\hat{H}$ vs $\mathcal{H}$ | 论文A vs 论文B | 统一使用 $\hat{H}$，$\mathcal{H}$ 仅用于变体 | 中 |
| 4 | $\delta$ (谱间隙) vs $\delta$ (其他) | 谱理论 vs BSD/其他 | 谱间隙用 $\delta$ 或 $\Delta\lambda$，其他上下文加下标 | 中 |
| 5 | $\lambda$ (特征值) vs $\lambda$ (扩展参数) | 谱理论 vs 图论 | 扩展图参数改用 $\lambda_{\text{exp}}$ 或 $\varepsilon$ | 中 |
| 6 | `ClassP = {L | True}` vs 数学定义 | Lean骨架 vs 论文 | 代码注释标明骨架状态，数学定义以文档为准 | 高 |
| 7 | `hardyZ` vs `zetaHardyZ` | RH.lean vs ZetaVerifier.lean | 统一使用 `zetaHardyZ`，`hardyZ`标记弃用 | 低 |
| 8 | `xi` (简化) vs 完整黎曼Xi | ZetaVerifier.lean | 代码注释标明简化版本 | 低 |
| 9 | $K(V)$ (代数簇) vs $K(L)$ (语言) | 论文C vs 论文A | 通过参数类型区分，论文中明确说明 | 中 |
| 10 | $\alpha$ (精细结构) vs $\alpha$ (子句-变量比) | 物理常数 vs 相变理论 | 相变理论改用 $r$ 或 $\rho$ 表示子句-变量比 | 中 |

---

## 5. 跨文件符号映射

### 5.1 Lean模块间映射

```
Basic.lean ─────┬──→ Complexity.lean: φ, Phi_c, D_c
               ├──→ RiemannHypothesis.lean: φ
               ├──→ CP004.lean: φ (间接)
               └──→ 所有模块: GF3

Complexity.lean ──→ CP004.lean: ClassP, ClassNP 概念继承
                ──→ CookLevin.lean: SAT, CNF 概念

CP004.lean ──────→ CP004_B2.lean: EntropyGap, P_neq_NP 概念

ZetaVerifier.lean ──→ RiemannHypothesis.lean: ZETA_ZERO_k, zetaHardyZ
```

### 5.2 论文到Lean映射

| 论文符号 | Lean符号 | 文件 |
|---------|---------|------|
| $K(L)$ | `descriptionComplexity` | CP004.lean |
| $\Delta H$ | `EntropyGap` | CP004.lean |
| $\mathbf{P}$ | `ClassP` | CP004.lean / Complexity.lean |
| $\mathbf{NP}$ | `ClassNP` | CP004.lean / Complexity.lean |
| $\leq_p$ | `≤ₚ` / `polyTimeReducible` | CP004_B2.lean |
| $\varphi$ | `Sylva.φ` | Basic.lean |
| $\Phi_c$ | `Phi_c` | Basic.lean |
| $\zeta(s)$ | `zeta` | RiemannHypothesis.lean |
| $\xi(s)$ | `xi` | ZetaVerifier.lean |
| $\gamma_1$ | `ZETA_ZERO_1` | NumericalZeros.lean |

---

## 6. 未来扩展预留

### 6.1 待定义符号（规划中）

| 符号 | 预期含义 | 预计引入位置 |
|------|---------|------------|
| $\hat{H}_{\text{eff}}$ | 有效哈密顿量 | SGH弱化证明完善 |
| $\delta_{\text{alg}}$ | 代数熵间隙 | 论文C扩展 |
| $\Delta H_{\text{quantum}}$ | 量子熵间隙 | BQP扩展 |
| $K_{\text{quantum}}(L)$ | 量子描述复杂度 | 量子扩展 |
| $\Phi_{\text{TOE}}$ | 万物理论临界值 | 15常数统一完成 |

### 6.2 版本升级计划

| 版本 | 目标 | 预计时间 |
|------|------|---------|
| v1.1 | 解决冲突1、2、6（Lean代码统一） | 2026-04-25 |
| v1.2 | 引入物理常数统一符号体系 | 2026-05-01 |
| v2.0 | 全部Lean代码与论文符号完全同步 | 2026-05-15 |

---

## 7. 维护指南

### 7.1 添加新符号流程

1. 检查本文档是否已存在冲突定义
2. 在对应章节添加符号条目
3. 如果存在冲突，在"冲突符号汇总"表中登记
4. 更新"跨文件符号映射"表
5. 在代码中添加注释引用本文档

### 7.2 修改现有符号流程

1. 在"冲突符号汇总"表中标记变更
2. 更新所有相关章节的定义
3. 更新"跨文件符号映射"表
4. 通知所有使用该符号的论文/代码维护者
5. 版本号递增

---

**文档结束**

> "符号是数学思想的服装。统一的符号体系不仅是方便，更是对思想一致性的约束。"
> — Sylva 形式化项目
