# 资料收集：Eliashberg理论严格边界 — Kiessling et al. 2024

> 收集日期：2026-06-04
> 收集方向：A路线（理论框架）+ 七层形式化
> 状态：✅ 已整理

---

## 1. Eliashberg理论Tc的严格上下界 — Kiessling et al. 2024

**来源**: Kiessling et al., "Bounds on Tc in the Eliashberg theory of Superconductivity. II", arXiv:2409.00532 (2024-08-31)
**机构**: Rutgers大学数学系 + 哥伦比亚大学物理系 + Rutgers材料理论中心
**被引**: 6次

### 核心贡献
- **严格证明**了Eliashberg理论中正常态与超导态的临界超曲面是函数 Λ(P,T) 的图像
- **变分原理**：临界温度由紧自伴算子 R(P,T) 的最大本征值 t(P,T) 决定
- **给出了Tc的严格下界序列**，收敛到真实Tc
- **给出了Tc的严格上界**（非最优，但符合渐近形式）

### 关键公式

**定义**：
- Eliashberg谱函数 α²F(ω) ≥ 0，满足 α²F(ω) ∝ ω²（小ω）
- 电子-声子耦合强度：λ = 2∫_{R₊} α²F(ω)/ω dω
- 概率测度：2α²F(ω)/ω =: λP'(ω)

**下界（N=1）**：
$$
T_c^{\flat}(\lambda, P) = \frac{1}{2\pi}(\lambda\langle\omega^2\rangle - \bar{\Omega}^2)^{1/2}
$$
其中 ⟨ω²⟩ = ∫ ω² P(dω)，Ω̄² 是P的支撑上界。

**上界**：
$$
T_c^{\sharp}(\lambda, P) = \frac{1}{2\pi}\sqrt{\lambda\langle\omega^2\rangle} \cdot C_{\infty}
$$
其中 C∞ ≈ 2.034 × 0.182726... 是渐近常数。

**渐近行为（强耦合极限）**：
$$
T_c(\lambda, P) \sim C_{\infty}\sqrt{\langle\omega^2\rangle}\sqrt{\lambda} \quad (\lambda \to \infty)
$$

---

## 2. 与论文的关联

### 直接填充内容

论文的 **七层形式化**（待编译）和 **A路理论框架** 可以引用：

1. **"Theorem 2.1 (Eliashberg极限的极限)"**：
   - Kiessling et al. 证明了对于**任意可容许P**，Tc(λ,P) 的严格存在性
   - 变分原理给出了可计算的上下界
   - 这与论文中 "λ → ∞ 时 Tc → √(λω²/3)" 的断言一致，但提供了更精确的常数

2. **"Allen-Dynes修正框架"**：
   - Kiessling et al. 纠正了Allen-Dynes公式中关于下界的声称
   - 证明了对2×2矩阵截断的逆映射存在性（Proposition 9）
   - 给出了3×3和4×4矩阵的显式下界（首次发表）

3. **"形式化代码"（07-目录）**：
   - 论文中的Eliashberg理论形式化（非Harmonic）可以从Kiessling的严格框架出发
   - 变分原理中的本征值问题可以形式化为线性算子理论

### 定理引用建议

论文中的 **Theorem 2.1** 可以扩展为：

> **Theorem 2.1' (Eliashberg Tc的严格边界)**: 
> 在标准Eliashberg模型中，设P为可容许概率测度，λ > 0，则：
> 1. 存在唯一的临界温度 Tc(λ,P) > 0，由变分原理 λ = 1/t(P,T) 定义
> 2. 对足够大的λ，Tc(λ,P) 满足以下严格边界：
>    - 下界：Tc(λ,P) > Tc^(⊥)(λ,P) = (1/2π)(λ⟨ω²⟩ - Ω̄²)^{1/2}
>    - 上界：Tc(λ,P) < Tc^(♯)(λ,P) = (1/2π)√(λ⟨ω²⟩) · C∞
> 3. 当 λ → ∞ 时，Tc(λ,P) ~ C∞√(⟨ω²⟩)√λ

---

## 3. Eliashberg理论的极限 — Sadovskii 2021

**来源**: M.V. Sadovskii, "Limits of Eliashberg Theory and Bounds for Superconducting Transition Temperature", arXiv:2106.09948

### 核心内容
- 综述了Eliashberg-McMillan理论的基础和局限性
- **强耦合极限**：当λ非常大时，晶格不稳定性限制有效耦合常数
- **非绝热近似**：Eliashberg理论在强反绝热极限也适用
- **超导转变温度的最大可能值**：讨论了Tc的理论上限

### 与论文的关联
- 为论文"Eliashberg理论"和"McMillan极限"小节提供权威综述
- Sadovskii指出：在稳定金属相中，有效配对常数可以取任意值
- 但**晶格不稳定性**（CDW、双极化子）在λ过大时会导致相变

---

## 4. 强耦合极限下的Tc下界

**Sadovskii (2021) 的强耦合结果**：

在强耦合极限（λ ≫ 1）下：
$$
T_c > \frac{0.18}{\sqrt{2}}\sqrt{\lambda\langle\omega^2\rangle}
$$

这与 Kiessling et al. (2024) 的下界一致，但Kiessling提供了更严格的框架。

---

## 5. 可直接使用的引用和公式

### 引用
1. **Kiessling et al. (2024)**: "Bounds on Tc in the Eliashberg theory of Superconductivity. II", arXiv:2409.00532.
2. **Sadovskii (2021)**: "Limits of Eliashberg Theory and Bounds for Superconducting Transition Temperature", arXiv:2106.09948.
3. **Allen-Dynes (1975)**: 原始Tc公式和修正框架。
4. **McMillan (1968)**: 原始Tc公式和极限。

### 关键公式集合

**McMillan公式**：
$$
T_c = \frac{\omega_{\log}}{1.2} \exp\left[ -\frac{1.04(1+\lambda)}{\lambda - \mu^*(1+0.62\lambda)} \right]
$$

**Allen-Dynes修正**：
$$
T_c = \frac{\omega_{\log}}{1.2} \exp\left[ -\frac{1.04(1+\lambda)}{\lambda - \mu^*(1+0.62\lambda)} \right] \cdot f_1 f_2
$$

**Kiessling严格下界（N=1）**：
$$
T_c > \frac{1}{2\pi}\sqrt{\lambda\langle\omega^2\rangle - \bar{\Omega}^2}
$$

**Kiessling严格上界**：
$$
T_c < \frac{1}{2\pi}\sqrt{\lambda\langle\omega^2\rangle} \cdot 2\sqrt{(2^{1+\varepsilon}-1)\zeta(1+\varepsilon)\zeta(5-\varepsilon)}
$$
其中 ε = 0.65。

---

## 6. 对论文形式化的建议

论文的 **07-形式化代码** 目录中，Eliashberg理论的非Harmonic版本可以：
1. 以 Kiessling et al. 的变分原理为基础
2. 将算子 R(P,T) 的最大本征值问题形式化
3. 证明 Tc 作为 λ 和 P 的函数的存在性和唯一性
4. 建立上下界的严格不等式链

这比直接从McMillan公式出发更严格，也更符合论文"数学完备性"的目标。

---

> **备注**: Kiessling et al. 的工作是数学物理的严格结果，适合论文的理论深度。建议在引用时同时提及物理直觉（McMillan/Allen-Dynes）和数学严格性（Kiessling）。
