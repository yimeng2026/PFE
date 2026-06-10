# BSD猜想最新进展文献综述

> 文献研究日期: 2026年4月11日
> 研究范围: arXiv最新论文、L函数计算、Sha群与Regulator研究、数值验证

---

## 一、arXiv最新论文 (2024-2026)

### 1.1 核心突破论文

#### 1. **Mazur-Tate精细猜想证明** (2025年11月)
- **论文**: *Swinnerton-Dyer type' conjectures of Mazur and Tate*
- **arXiv**: arXiv:2511.07203
- **作者**: Dominik Bullach等
- **核心成果**: 证明了Mazur和Tate提出的BSD猜想精细版本的大部分内容
- **方法**: 通过等变Tamagawa数猜想的"秩零分量"途径
- **意义**: 这是BSD猜想研究的重要进展，提供了比原始BSD猜想更精细的公式

#### 2. **复乘椭圆曲线的BSD证明** (2024年)
- **论文**: *The conjecture of Birch and Swinnerton-Dyer for certain elliptic curves with complex multiplication*
- **期刊**: Cambridge J. Math. 12 (2024), 357-415
- **作者**: A. Burungale, M. Flach
- **核心成果**: 对某些具有复乘的椭圆曲线证明了BSD猜想
- **方法**: 使用Gross-Zagier公式和Euler系统理论

#### 3. **Zeta元素与椭圆曲线应用** (2024年)
- **论文**: *Zeta elements for elliptic curves and applications*
- **arXiv**: arXiv:2409.01350
- **作者**: A. Burungale, C. Skinner, Y. Tian, X. Wan
- **核心成果**: 发展了椭圆曲线的Zeta元素理论
- **应用**: 应用于BSD猜想的p-part证明

#### 4. **无限扭曲满足BSD的椭圆曲线** (2026年1月)
- **论文**: *On the identification of elliptic curves that admit infinitely many twists satisfying the Birch–Swinnerton-Dyer conjecture*
- **arXiv**: arXiv:2601.16044
- **作者**: B. Banwait, X. Huang
- **核心成果**: 识别出允许无限多个满足BSD猜想的二次扭曲的椭圆曲线
- **数据**: 已列出导体不超过500,000的椭圆曲线列表
- **GitHub**: https://github.com/cocoxhuang/ants_xvii

### 1.2 相关L函数研究

#### 5. **模ℓ非零性结果** (2026年3月)
- **论文**: *Mod ℓ non-vanishing of self-dual Hecke L-values over CM fields*
- **arXiv**: arXiv:2508.19706
- **核心内容**: 研究CM域上自对偶Hecke L-值的模ℓ非零性
- **应用**: 对BSD猜想的应用

#### 6. **Tamagawa数猜想** (2025年10月)
- **论文**: *On the Tamagawa number conjecture for modular forms*
- **arXiv**: arXiv:2510.01601
- **作者**: F. Castella, C.-Y. Hsu, D. Kundu等
- **核心成果**: 研究模形式的Tamagawa数猜想
- **方法**: 导出p-adic高度与Bertolini-Darmon-Prasanna p-adic L函数的联系

---

## 二、椭圆曲线L函数计算

### 2.1 算法进展

#### 1. **Schoof算法扩展** (2021-2023)
- **论文**: *L-Functions of Elliptic Curves Modulo Integers*
- **arXiv**: arXiv:2110.12156
- **作者**: Félix Baril Boudreau
- **核心贡献**:
  - 扩展Schoof算法到函数域上椭圆曲线的L函数模整数计算
  - 提供二次扭曲L函数模2的显式公式
  - 可高效计算全局根数和分析秩

#### 2. **余数树算法** (Edgar Costa, 2024)
- **来源**: Computing L-functions - SUNY系列讲座 (2024年11月)
- **算法**: 余数树(Remainder Tree)算法
- **应用范围**:
  - 超椭圆曲线L函数: $y^2 = f(x)$
  - 超椭圆曲线L函数: $y^r = f(x)$
  - 光滑平面四次曲线
  - 超几何 motive
- **复杂度**: 计算所有 $p < B$ 的 $a_p$ 需要 $B(\log B)^{3+o(1)}$ 时间

#### 3. **函数域L函数计算** (2023)
- **论文**: *Journal of Number Theory* (2023)
- **核心方法**:
  - 基于Hall定理的模N公式
  - 适用于非恒定j-不变量的椭圆曲线
  - 可计算次数2的L函数

### 2.2 计算方法综述

| 方法 | 适用对象 | 时间复杂度 | 关键特征 |
|------|----------|-----------|----------|
| Schoof算法 | 有限域椭圆曲线 | $O(\log^8 p)$ | 直接计算模素数 |
| 余数树 | 超椭圆曲线 | $B(\log B)^{3+o(1)}$ | 批处理计算 |
| 模符号 | 模形式L函数 | 多项式时间 | 基于模符号理论 |
| 启发式方法 | 高亏格曲线 | 可变 | 数值验证为主 |

---

## 三、Sha群与Regulator研究

### 3.1 Sha群（Tate-Shafarevich群）研究

#### 1. **机器学习方法预测Sha阶** (2024年12月)
- **论文**: *Machine Learning Approaches to the Shafarevich-Tate Group*
- **arXiv**: arXiv:2412.18576
- **核心发现**:
  - 使用BSD公式中的各项特征训练模型
  - 对秩为0的曲线，实周期(Real Period)最具预测力
  - 对正秩曲线，Tamagawa积最具预测力
  - 开发了预测Sha阶的回归模型

#### 2. **应用案例：秩29 Elkies-Klagsbrun曲线**
- **曲线**: $E_{29}$ (记录级秩29曲线)
- **计算值**:
  - Regulator: $433744182671713097629179252379019849.49...$
  - 实周期: $3.509... \times 10^{-15}$
  - Tamagawa积: $10725120$
  - 扭子群: 平凡

#### 3. **Iwasawa μ-不变量研究** (2025年1月)
- **论文**: *A bound on the μ-invariants of supersingular elliptic curves*
- **arXiv**: arXiv:2409.18021
- **相关性**: μ-不变量与Sha群的p-primary部分密切相关

### 3.2 Regulator研究

#### 1. **p-adic Regulator** (计算论文)
- **来源**: Computing Tate-Shafarevich Groups (Nottingham)
- **关键公式**:
  - 对乘性约化素数使用Tate p-adic一致化
  - 修正的p-adic高度配对公式
  - p-adic sigma函数定义:
    $$\sigma_p(u) = \frac{u-1}{u^{1/2}} \prod_{n \geq 1} \frac{(1-q_E^n u)(1-q_E^n/u)}{(1-q^n)^2}$$

#### 2. **虚二次域上的Regulator** (2025年7月)
- **论文**: *Regulators of the Fixed Elliptic Curve over Rank-One Imaginary Quadratic Fields*
- **arXiv**: arXiv:2507.20297
- **发现**: 在秩一虚二次域上，L-导数与Regulator的比值是固定常数

### 3.3 BSD公式的算术不变量

完整的BSD公式涉及以下不变量:

$$\lim_{s \to 1} \frac{L(E,s)}{(s-1)^r} = \frac{\#\text{Ш}(E) \cdot R \cdot \prod c_p}{(\#E(\mathbb{Q})_{tors})^2}$$

其中:
- $R$: Regulator (实值)
- $\prod c_p$: Tamagawa数乘积
- $\#E(\mathbb{Q})_{tors}$: 扭子群阶
- $\#\text{Ш}(E)$: Tate-Shafarevich群阶 (猜想有限)

---

## 四、数值验证结果

### 4.1 大规模数值验证

#### 1. **高亏格超椭圆曲线验证** (2017年)
- **论文**: *Numerical verification of the Birch and Swinnerton-Dyer conjecture for hyperelliptic curves*
- **arXiv**: arXiv:1711.10409
- **成果**:
  - 首次验证亏格3、4、5的曲线
  - 验证了32条亏格2曲线的BSD猜想
  - 计算了实周期、Regulator、Tamagawa数
  - Sha的猜想阶与整数的误差小于 $10^{-9}$

#### 2. **导体≤1000的曲线** (BSD计算项目)
- **来源**: Sage Summer Workshop on BSD
- **状态**:
  - 2463条最优曲线，导体≤1000
  - 18条秩为2的曲线
  - 计划验证秩0或1的2445条曲线
- **障碍**: 秩>1时，尚未证明Ш的有限性

### 4.2 验证方法

#### 1. **秩0曲线**
- 验证 $L(E,1) \neq 0$
- 使用Kato定理

#### 2. **秩1曲线**
- 验证 $L(E,1) = 0$ 且 $L'(E,1) \neq 0$
- 使用Gross-Zagier公式和Kolyvagin定理

#### 3. **高秩曲线**
- 数值计算L函数高阶导数
- 比较猜想Sha阶与理性平方

### 4.3 当前验证范围

| 曲线类型 | 最大导体/亏格 | 验证状态 |
|----------|--------------|----------|
| 椭圆曲线 (秩0,1) | 1000 | 计划完成 |
| 亏格2曲线 | 小导体 | 已验证 |
| 亏格3曲线 | 多条实例 | 首次验证 |
| 亏格4,5曲线 | 多条实例 | 首次验证 |
| 超椭圆曲线 (高亏格) | 多种 | 模平方验证 |

---

## 五、理论进展与开放问题

### 5.1 已证明结果

1. **秩≤1的弱BSD**: Kolyvagin (1989-1991) 和 Gross-Zagier (1986)
   - 代数秩 = 分析秩
   - Ш有限

2. **复乘曲线的BSD**: Burungale-Flach (2024)
   - 对某些复乘椭圆曲线证明了完整BSD

3. **p-part BSD**: Jetchev-Skinner-Wan (2017)
   - 对半稳定椭圆曲线秩1情况证明p-part

### 5.2 开放问题

1. **Ш的有限性**: 秩>1时尚未证明
2. **高秩BSD**: 秩≥2的完整BSD仍是开放问题
3. **精确公式**: 强BSD公式的主项系数
4. **一般数域**: 非Q上的椭圆曲线

### 5.3 研究前沿

1. **Iwasawa理论**: p-adic L函数与主猜想
2. **Euler系统**: Kolyvagin系统的推广
3. **机器学习**: 数据驱动的BSD不变量预测
4. **计算数论**: 更大规模数值验证

---

## 六、关键参考文献

### 经典文献
1. Birch, B.J., Swinnerton-Dyer, H.P.F. (1965). *Notes on elliptic curves. II*. J. Reine Angew. Math. 218, 79-108.

2. Tate, J. (1966). *On the conjectures of Birch and Swinnerton-Dyer and a geometric analog*.

3. Gross, B., Zagier, D. (1986). *Heegner points and derivatives of L-series*. Invent. Math. 84, 225-320.

### 近期重要论文
4. Burungale, A., Flach, M. (2024). *The conjecture of Birch and Swinnerton-Dyer for certain elliptic curves with complex multiplication*. Camb. J. Math. 12(2), 357-415.

5. Bullach, D. et al. (2025). *Swinnerton-Dyer type conjectures of Mazur and Tate*. arXiv:2511.07203.

6. Jetchev, D., Skinner, C., Wan, X. (2017). *The Birch and Swinnerton-Dyer formula for elliptic curves of analytic rank one*. Camb. J. Math. 5(3), 369-434.

### 计算与数值
7. Flynn, E.V. et al. (2001). *Empirical evidence for the Birch and Swinnerton-Dyer conjectures for modular Jacobians of genus 2 curves*. Math. Comp. 70(236), 1675-1697.

8. Costa, E. (2024). *Computing L-functions* (Lecture Notes).

---

## 七、结论

BSD猜想研究在2024-2026年间取得了重要进展：

1. **理论突破**: Mazur-Tate精细猜想的实质性证明
2. **复乘曲线**: 更大类复乘椭圆曲线的BSD证明
3. **计算方法**: 余数树算法等高效计算技术的发展
4. **机器学习**: 数据科学方法在Sha预测中的应用
5. **数值验证**: 首次扩展到亏格3、4、5曲线

然而，一般椭圆曲线的BSD猜想，特别是秩≥2的情况，仍是数论中最具挑战性的问题之一。

---

*文献综述完成*
