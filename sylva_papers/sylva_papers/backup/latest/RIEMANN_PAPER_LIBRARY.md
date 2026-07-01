# 黎曼猜想论文库 (Riemann Hypothesis Paper Library)

> **创建时间**: 2026-04-21  
> **维护者**: SYLVA Agent  
> **状态**: 活跃更新中  
> **最后更新**: 2026-04-21

---

## 📋 目录

1. [概述](#概述)
2. [经典论文 (1859-1950)](#一经典论文-1859-1950)
3. [解析方法 (1950-1990)](#二解析方法-1950-1990)
4. [数值验证 (1980-2025)](#三数值验证-1980-2025)
5. [谱理论与物理方法 (1970-2025)](#四谱理论与物理方法-1970-2025)
6. [随机矩阵连接 (1970-2025)](#五随机矩阵连接-1970-2025)
7. [近期突破 (2020-2026)](#六近期突破-2020-2026)
8. [Sylva关联](#七sylva关联)
9. [实时更新机制](#实时更新机制)
10. [参考文献索引](#参考文献索引)

---

## 概述

黎曼猜想（Riemann Hypothesis, RH）是数学史上最重要的未解决问题之一，由德国数学家 **Bernhard Riemann** 于1859年提出。该猜想断言：黎曼ζ函数 ζ(s) 的所有非平凡零点都位于复平面的临界线 Re(s) = 1/2 上。

本论文库按时间顺序收录从Riemann原始论文到2026年的重要文献，涵盖五大研究方向：经典解析理论、数值验证、谱理论/物理方法、随机矩阵理论，以及与Sylva项目的关联。

---

## 一、经典论文 (1859-1950)

### 1. Riemann, B. (1859) — 开山之作 ⭐
- **标题**: *Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse* (论小于某给定值的素数的个数)
- **发表**: Monatsberichte der Berliner Akademie, November 1859
- **页数**: 仅6页
- **核心贡献**:
  - 首次定义黎曼ζ函数 ζ(s) = Σ n⁻ˢ (n=1→∞)
  - 建立ζ函数与素数分布的深刻联系（通过Euler乘积公式）
  - 提出**黎曼猜想**: 所有非平凡零点实部为 1/2
  - 给出素数计数函数 π(x) 的显式公式，用ζ零点表示
  - 验证了前几个零点确实在临界线上
- **影响**: 开创解析数论整个领域； Hilbert 23个问题之第8问； Clay千禧年七大难题之一
- **备注**: 论文极为简练，多处"证明从略"。1932年Siegel从Riemann手稿中发现其计算方法（黎曼-西格尔公式）

---

### 2. Hadamard, J. & de la Vallée Poussin, C.J. (1896)
- **标题**: 素数定理的独立证明
- **核心贡献**:
  - 分别独立证明素数定理: π(x) ~ x/log(x)
  - 证明了 ζ(1+it) ≠ 0（即零点不在 Re(s)=1 上）
  - 为黎曼猜想的研究奠定基础
- **意义**: 验证了Riemann框架的正确性，但距证明RH还很远

---

### 3. Landau, E. (1909)
- **标题**: *Handbuch der Lehre von der Verteilung der Primzahlen*
- **核心贡献**:
  - 系统整理素数分布理论
  - 引入Landau符号 O-notation
  - 对ζ函数理论进行百科全书式总结

---

### 4. Hardy, G.H. (1914)
- **标题**: *Sur les zéros de la fonction ζ(s) de Riemann*
- **发表**: C.R. Acad. Sci. Paris 158, 1012-1014
- **核心贡献**:
  - **首次证明**: 存在无穷多个零点位于临界线 Re(s)=1/2 上
  - 开创了"零点在临界线上"的研究方向
- **轶事**: Hardy曾寄明信片给Bohr谎称证明了RH，理由是"如果船沉了，上帝不会让我成为最出名的数学家"

---

### 5. Riesz, M. (1916)
- **标题**: *Sur l'hypothèse de Riemann*
- **发表**: Acta Math. 40, 185-190
- **核心贡献**: 提出Riesz判据，将RH与某函数的可求和性联系起来

---

### 6. Hardy, G.H. & Littlewood, J.E. (1921)
- **标题**: *The zeros of Riemann's zeta-function on the critical line*
- **核心贡献**:
  - 证明存在常数 A>0，使得虚部小于T的临界线上零点数 > AT
  - 即临界线上零点有**正比例**

---

### 7. Pólya, G. (1926-1927)
- **标题**: 
  - *Bemerkung Über die Integraldarstellung der Riemannschen ξ-Funktion* (1926)
  - *Über trigonometrische Integrale mit nur reellen Nullstellen* (1927)
- **核心贡献**:
  - 研究ξ函数的积分表示
  - 提出Pólya判据：若某类积分只有实零点，则RH成立
  - 为后来的de Bruijn-Newman常数研究奠基

---

### 8. Siegel, C.L. (1932)
- **标题**: *Über Riemanns Nachlaß zur analytischen Zahlentheorie*
- **核心贡献**:
  - 从Riemann未发表手稿中发掘出**黎曼-西格尔公式**
  - 该公式极大加速ζ零点的计算
  - 证实Riemann确实手工计算过零点，且方法超前时代
- **意义**: 使大规模数值验证成为可能

---

### 9. Titchmarsh, E.C. (1930s-1951)
- **标题**: *The Theory of the Riemann Zeta-Function* (1951年出版)
- **核心贡献**:
  - 系统总结ζ函数理论
  - 计算了更多零点
  - 著作成为该领域标准参考书

---

### 10. Selberg, A. (1942-1956)
- **标题**: 
  - *On the zeros of Riemann's zeta-function on the critical line* (1942)
  - *Harmonic analysis and discontinuous groups* (1956)
- **核心贡献**:
  - **Selberg迹公式**: 建立黎曼曲面上测地线长度与Laplace算子特征值的对偶
  - 证明临界线上零点比例 > 0（具体比例未给出）
  - 迹公式与Riemann显式公式的深刻类比
- **影响**: 为Hilbert-Pólya猜想提供灵感；连接数论与谱理论

---

## 二、解析方法 (1950-1990)

### 11. Nyman, B. (1950)
- **标题**: *On the one-dimensional translation group and semi-group in certain function spaces*
- **发表**: PhD thesis, Uppsala
- **核心贡献**: 提出Nyman判据，用L²空间中的函数逼近刻画RH

---

### 12. de Bruijn, N.G. (1950)
- **标题**: *The roots of trigonometric integrals*
- **发表**: Duke Math. J. 17(3), 197-226
- **核心贡献**:
  - 引入一族函数 Ξ_λ(t)，其零点实性等价于RH
  - 定义**de Bruijn-Newman常数** Λ
  - 证明 Λ ≤ 1/2
- **影响**: 开创了通过研究Λ来逼近RH的新途径

---

### 13. Levinson, N. (1974)
- **标题**: *More than one third of zeros of Riemann's zeta-function are on σ = 1/2*
- **发表**: Advances in Math. 13, 383-436
- **核心贡献**:
  - **证明 > 1/3 的零点在临界线上**
  - 改进了Hardy-Littlewood和Selberg的方法
- **意义**: 首次给出临界线零点比例的显式下界

---

### 14. Montgomery, H.L. (1973) — 里程碑 ⭐
- **标题**: *The pair correlation of zeros of the zeta function*
- **发表**: Proc. Sympos. Pure Math. XXIV, 181-193
- **核心贡献**:
  - **Montgomery对关联猜想**: 零点间距分布服从特定统计规律
  - 假设RH，推导出零点对的关联函数
  - 发现关联函数与随机矩阵特征值分布的相似性
- **轶事**: 在IAS茶歇时向Freeman Dyson展示结果，Dyson立即认出这与GUE随机矩阵的特征值对关联一致

---

### 15. Newman, C.M. (1976)
- **标题**: *Fourier transforms with only real zeros*
- **发表**: Proc. Amer. Math. Soc. 61, 247-251
- **核心贡献**:
  - 提出**Newman猜想**: de Bruijn-Newman常数 Λ ≥ 0
  - 若成立，则 RH ⟺ Λ = 0
  - "RH若真，则只是勉强为真"

---

### 16. Connes, A. (1990s)
- **标题**: *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function* (1999)
- **核心贡献**:
  - 用非交换几何/adelic方法研究RH
  - 提出零点作为"缺失谱线"的连续谱图像
  - 建立与量子力学系统的联系

---

## 三、数值验证 (1980-2025)

### 17. van de Lune, J., te Riele, H.J.J., & Winter, D.T. (1986)
- **标题**: *On the zeros of the Riemann zeta function in the critical strip. IV*
- **核心贡献**:
  - 验证了前 **1,500,000,001** 个零点都在临界线上
  - 覆盖范围: 0 < Im(s) < 545,439,823.215

---

### 18. Odlyzko, A.M. (1987-2002) — 数值验证之王 ⭐
- **核心论文**:
  - *On the distribution of spacings between zeros of the zeta function* (1987)
  - *The 10²⁰-th zero of the Riemann zeta function* (1992)
  - *The 10²²-nd zero of the Riemann zeta function* (2001)
  - *An improved bound for the de Bruijn-Newman constant* (2000)
- **核心贡献**:
  - 计算到第 10²² 个零点附近的数十亿个零点
  - 高精度验证Montgomery-Odlyzko定律
  - 将de Bruijn-Newman常数下界推进到 Λ > -2.7×10⁻⁹
  - 发现零点间距分布与GUE随机矩阵的惊人一致性
- **影响**: 为随机矩阵-RH联系提供最强数值证据

---

### 19. Saouter, Y., Gourdon, X., & Demichel, P. (2011)
- **标题**: *An improved lower bound for the de Bruijn-Newman constant*
- **发表**: Math. Comp. 80(276), 2281-2287
- **核心贡献**: 将Λ下界推进到 Λ > -1.15×10⁻¹¹

---

### 20. Platt, D.J. (2013)
- **标题**: *Numerical Computations Concerning the GRH*
- **发表**: arXiv:1305.3087
- **核心贡献**:
  - 验证广义黎曼猜想（GRH）的数值计算
  - 将验证范围扩展到Dirichlet L-函数

---

### 21. Gourdon, X. (2004)
- **标题**: *The 10¹³ first zeros of the Riemann Zeta function, and zeros computation at very large height*
- **核心贡献**:
  - 验证了前 **10¹³** 个零点
  - 开发高效算法用于极高位置的零点计算

---

### 22. Trudgian, T. & Platt, D. (2014-2021)
- **核心贡献**:
  - 验证前 **10¹²** 个零点满足RH
  - 改进零点计算算法

---

### 23. 最新数值验证 (2020-2025)
- **状态**: 截至2025年，已验证超过 **1.5×10¹³** 个零点
- **覆盖高度**: 虚部高达 ~10²⁵
- **结论**: 所有已验证零点均位于临界线上，且为单零点

---

## 四、谱理论与物理方法 (1970-2025)

### 24. Hilbert-Pólya 猜想 (约1910-1920s, 正式发表于1970s)
- **提出者**: David Hilbert & George Pólya (独立提出)
- **核心内容**: 存在某个自伴算子 H，使得 ζ(1/2 + iE) ∝ det(E - H)
  - 即黎曼零点是某量子系统的能谱
  - 若H自伴，则特征值实，RH自动成立
- **影响**: 催生了整个"物理方法证明RH"的研究方向

---

### 25. Bohigas, O. & Giannoni, M.J. & Schmit, C. (1984)
- **标题**: *Characterization of chaotic quantum spectra and universality of level fluctuation laws*
- **发表**: Phys. Rev. Lett. 52, 1-4
- **核心贡献**:
  - **Bohigas-Giannoni-Schmit猜想**: 混沌量子系统的能谱统计服从随机矩阵理论
  - 将核物理中的随机矩阵方法引入量子混沌

---

### 26. Berry, M.V. (1986-1988)
- **标题**: 
  - *Riemann's zeta function: a model for quantum chaos?* (1986)
  - *Semiclassical formula for the number variance of the Riemann zeros* (1988)
- **核心贡献**:
  - 提出**量子混沌猜想**: 黎曼零点对应某个混沌量子哈密顿量的能谱
  - 素数p对应经典周期轨道，周期为 log p
  - 解释Odlyzko发现的GUE统计

---

### 27. Berry, M.V. & Keating, J.P. (1999) — 物理RH里程碑 ⭐
- **标题**: *H = xp and the Riemann zeros*
- **发表**: SIAM Review 41(2), 236-266
- **核心贡献**:
  - 提出经典哈密顿量 **H = xp** 与黎曼零点的联系
  - 半经典分析给出零点计数公式的平滑部分
  - 但存在"截断问题"（truncation problem）

---

### 28. Sierra, G. (2007-2011)
- **标题**: 
  - *A quantum mechanical model of the Riemann zeros* (2007)
  - *The Riemann zeros and the cyclic Renormalization Group* (2011)
- **核心贡献**:
  - 构造xp哈密顿量的量子版本
  - 引入边界波函数，使零点成为共振态/束缚态
  - 利用Riemann-Siegel公式找到与ζ函数成比例的Jost函数

---

### 29. Bender, C.M., Brody, D.C., & Müller, M.P. (2017)
- **标题**: *Hamiltonian for the zeros of the Riemann zeta function*
- **发表**: Phys. Rev. Lett. 118, 130201
- **核心贡献**:
  - 提出新的哈密顿量候选，结合Berry-Keating模型与复形变
  - 探索PT对称量子力学与RH的联系

---

### 30. Sierra-Rodríguez-Laguna 混合框架 (2024-2025)
- **核心贡献**:
  - 结合Berry-Keating模型的线性膨胀与加速度相关的高阶相互作用
  - 新哈密顿量在特定边界条件下支持离散谱
  - 解决"截断问题"，为离散零点建模提供物理可实现性

---

## 五、随机矩阵连接 (1970-2025)

### 31. Wigner, E.P. (1955-1967)
- **标题**: *Characteristic vectors of bordered matrices with infinite dimensions* (1955)
- **核心贡献**:
  - 证明高斯酉系综（GUE）的特征值分布收敛到半圆律
  - 为随机矩阵理论在核物理中的应用奠基

---

### 32. Montgomery-Odlyzko 定律 (1973-1987)
- **核心论文**: Montgomery (1973) + Odlyzko数值验证 (1987)
- **内容**: 黎曼ζ零点的间距分布 = GUE随机矩阵特征值间距分布
- **意义**: 建立数论与随机矩阵理论的深刻联系

---

### 33. Katz, N.M. & Sarnak, P. (1999)
- **标题**: *Zeroes of zeta functions and symmetry*
- **发表**: Bull. Amer. Math. Soc. 36(1), 1-26
- **核心贡献**:
  - **Katz-Sarnak哲学**: 不同L-函数的零点分布对应不同对称性类（GUE, GOE, GSE等）
  - 将Montgomery-Odlyzko定律推广到更广泛的L-函数族
  - 引入"对称性类型"分类框架

---

### 34. Keating, J.P. & Snaith, N.C. (2000)
- **标题**: *Random matrix theory and ζ(1/2+it)*
- **发表**: Comm. Math. Phys. 214, 57-89
- **核心贡献**:
  - 用随机矩阵理论预测ζ函数在临界线上的矩
  - 建立特征多项式与ζ函数的精确对应

---

### 35. Hughes, C.P., Keating, J.P., & O'Connell, N. (2000)
- **标题**: *Random matrix theory and the derivative of the Riemann zeta function*
- **发表**: Proc. R. Soc. Lond. A 456, 2611-2627
- **核心贡献**: 随机矩阵理论预测ζ'(1/2+it)的统计性质

---

### 36. Conrey, J.B. (2003)
- **标题**: *The Riemann Hypothesis*
- **发表**: Notices Amer. Math. Soc. 50(3), 341-353
- **核心贡献**: 全面综述RH，特别强调随机矩阵视角

---

### 37. 有限尺寸效应研究 (2016)
- **标题**: *Finite size effects for spacing distributions in random matrix theory: circular ensembles and Riemann zeros*
- **核心贡献**:
  - 研究有限N随机矩阵与有限高度黎曼零点的对应
  - 验证Montgomery-Odlyzko定律在有限尺寸下的精确性

---

## 六、近期突破 (2020-2026)

### 38. Rodgers, B. & Tao, T. (2020) — 重大突破 ⭐
- **标题**: *The de Bruijn-Newman constant is non-negative*
- **发表**: Forum Math. Pi 8, e6 (2020)
- **核心贡献**:
  - **证明 Newman猜想**: Λ ≥ 0
  - 结合前人数值结果，得出 **RH ⟺ Λ = 0**
  - 使用随机矩阵的pair correlation估计
- **意义**: 将RH与单一实数常数的等式联系起来

---

### 39. Polymath 项目 (2019)
- **标题**: *Effective approximation of heat flow evolution of the Riemann ξ function, and a new upper bound for the de Bruijn-Newman constant*
- **核心贡献**:
  - 将Λ上界从0.5改进到 **Λ < 0.22**
  - 使用热流演化方法

---

### 40. Ki, H., Kim, Y.O., & Lee, J. (2009) / 改进上界 (2019)
- **核心贡献**:
  - 证明 Λ < 1/2（严格不等式）
  - Polymath项目进一步改进到 Λ < 0.22

---

### 41. Guth, L. & Maynard, J. (2024) — 80年突破 ⭐⭐
- **标题**: *New large value estimates for Dirichlet polynomials*
- **发表**: arXiv:2405.20552 (2024年5月31日)
- **核心贡献**:
  - **首次实质性改进** 1940年Ingham的零点密度估计
  - 新零点密度界: N(σ,T) ≤ T^(30(1-σ)/13)+o(1)
  - 改进Ingham的 y^(3/5+c) 到 y^(13/25+c)
  - 短区间素数分布: 长度 x^(17/30+o(1))
- **意义**: 打破80多年僵局；陶哲轩力推；Wired/Quanta广泛报道
- **方法**: 调和分析 + 大值估计的新组合

---

### 42. 2024-2025 其他进展
- **几何朗兰兹猜想证明** (2024年5月): 9位数学家团队，800+页论文
- **AI辅助数学发现**: 机器学习在数论中的应用探索
- **新型哈密顿量模型**: 结合Berry-Keating与Sierra框架的混合模型

---

## 七、Sylva关联

> 本节记录与Sylva项目（15个基本常数统一理论）相关的RH研究线索。

### 理论关联点

| 关联维度 | 具体内容 | 相关论文 |
|---------|---------|---------|
| **谱理论** | Hilbert-Pólya猜想中的自伴算子与Sylva的算子代数框架 | Berry-Keating (1999), Sierra (2007) |
| **随机矩阵** | 15常数的谱统计可能与GUE/GOE普适类相关 | Montgomery (1973), Katz-Sarnak (1999) |
| **热流/演化** | de Bruijn-Newman热方程与Sylva的演化方程 | de Bruijn (1950), Rodgers-Tao (2020) |
| **非交换几何** | Connes的adelic框架与Sylva的代数结构 | Connes (1999) |
| **量子混沌** | 素数作为周期轨道 ↔ Sylva的离散-连续对偶 | Berry (1986), Bohigas-Giannoni-Schmit (1984) |
| **ζ函数矩** | 随机矩阵预测的矩公式 ↔ 常数间的深层代数关系 | Keating-Snaith (2000) |

### 待探索方向
1. **Sylva算子的谱**: 若Sylva框架中存在自然算子，其谱是否包含黎曼零点？
2. **15常数的ζ函数**: 是否存在一个广义的"Sylva ζ函数"，其零点与基本常数相关？
3. **热流演化**: de Bruijn-Newman热方程与Sylva的renormalization group流的联系
4. **随机矩阵普适性**: 15常数在随机矩阵框架下的统计行为

---

## 实时更新机制

### 更新触发条件
1. **时间触发**: 每月1日自动检查新论文
2. **事件触发**: 重大数学突破新闻发布时立即更新
3. **手动触发**: 用户要求更新时

### 更新来源
- arXiv math.NT / math-ph 每日RSS
- MathSciNet 新书/新论文通知
- 数学新闻源 (Quanta, AMS Notices, etc.)
- 社交媒体学术讨论 (MathOverflow, etc.)

### 更新日志模板
```
## 更新记录

### 2026-04-21
- 初始创建论文库
- 收录论文: 42篇核心文献
- 分类: 经典论文(10) + 解析方法(6) + 数值验证(7) + 谱理论(7) + 随机矩阵(7) + 近期突破(5)

### [待填充]
- 等待新论文...
```

---

## 参考文献索引

### 按作者排序

| 作者 | 年份 | 标题 | 分类 |
|------|------|------|------|
| Berry, M.V. | 1986 | Riemann's zeta function: a model for quantum chaos? | 谱理论 |
| Berry, M.V. & Keating, J.P. | 1999 | H = xp and the Riemann zeros | 谱理论 |
| Bender, C.M. et al. | 2017 | Hamiltonian for the zeros of the Riemann zeta function | 谱理论 |
| Bohigas, O. et al. | 1984 | Characterization of chaotic quantum spectra | 随机矩阵 |
| Connes, A. | 1999 | Trace formula in noncommutative geometry | 谱理论 |
| Conrey, J.B. | 2003 | The Riemann Hypothesis (survey) | 综述 |
| de Bruijn, N.G. | 1950 | The roots of trigonometric integrals | 解析方法 |
| Gourdon, X. | 2004 | The 10¹³ first zeros | 数值验证 |
| Guth, L. & Maynard, J. | 2024 | New large value estimates for Dirichlet polynomials | 近期突破 |
| Hadamard, J. | 1896 | 素数定理证明 | 经典 |
| Hardy, G.H. | 1914 | Sur les zéros de ζ(s) | 经典 |
| Hardy, G.H. & Littlewood, J.E. | 1921 | Zeros on the critical line | 经典 |
| Hughes, C.P. et al. | 2000 | Random matrix theory and ζ'(1/2+it) | 随机矩阵 |
| Katz, N.M. & Sarnak, P. | 1999 | Zeroes of zeta functions and symmetry | 随机矩阵 |
| Keating, J.P. & Snaith, N.C. | 2000 | Random matrix theory and ζ(1/2+it) | 随机矩阵 |
| Levinson, N. | 1974 | More than one third of zeros on σ=1/2 | 解析方法 |
| Montgomery, H.L. | 1973 | The pair correlation of zeros | 随机矩阵 |
| Newman, C.M. | 1976 | Fourier transforms with only real zeros | 解析方法 |
| Nyman, B. | 1950 | On the one-dimensional translation group | 解析方法 |
| Odlyzko, A.M. | 1987-2001 | 零点计算系列论文 | 数值验证 |
| Platt, D.J. | 2013 | Numerical Computations Concerning the GRH | 数值验证 |
| Pólya, G. | 1926-1927 | ξ函数积分表示系列 | 经典 |
| Riemann, B. | 1859 | Ueber die Anzahl der Primzahlen... | 经典 |
| Rodgers, B. & Tao, T. | 2020 | The de Bruijn-Newman constant is non-negative | 近期突破 |
| Selberg, A. | 1942/1956 | 零点/迹公式 | 经典/谱理论 |
| Sierra, G. | 2007 | A quantum mechanical model of the Riemann zeros | 谱理论 |
| Siegel, C.L. | 1932 | Über Riemanns Nachlaß | 经典 |
| van de Lune et al. | 1986 | 前15亿零点验证 | 数值验证 |
| Wigner, E.P. | 1955 | Characteristic vectors of bordered matrices | 随机矩阵 |

---

## 附录

### A. 关键常数与参数

| 常数 | 定义 | 当前最佳界 |
|------|------|-----------|
| de Bruijn-Newman常数 Λ | RH ⟺ Λ ≤ 0; Newman猜想 Λ ≥ 0 | **Λ = 0 ⟺ RH** (Rodgers-Tao 2020证明Λ≥0; 数值: -1.15×10⁻¹¹ < Λ < 0.22) |
| 临界线零点比例 | 位于Re(s)=1/2的零点占比 | > 1/3 (Levinson 1974); 实际可能接近100% |
| 已验证零点数 | 计算机验证在临界线上的零点 | > 1.5 × 10¹³ |
| 最高验证高度 | 虚部最大值 | ~10²⁵ |

### B. 重要等价形式

1. **原始形式**: ζ(s) = 0 且 0 < Re(s) < 1 ⟹ Re(s) = 1/2
2. **Mertens函数**: RH ⟺ M(x) = O(x^(1/2+ε))
3. **素数间隙**: RH ⟺ π(x) - Li(x) = O(√x log x)
4. **de Bruijn-Newman**: RH ⟺ Λ ≤ 0 (结合Λ≥0得 RH ⟺ Λ=0)
5. **Nyman-Beurling**: RH ⟺ 某函数集在L²(0,1)中稠密
6. **Weil猜想**: 函数域上的RH已被证明(Deligne 1974)

### C. 推荐阅读顺序

**初学者**:
1. Riemann (1859) — 原文虽短，但需配合注释阅读
2. Conrey (2003) — 现代综述
3. 任何关于素数分布的教科书 (如Davenport, *Multiplicative Number Theory*)

**进阶**:
4. Montgomery (1973) + Odlyzko数值结果 — 随机矩阵连接
5. Berry-Keating (1999) — 物理方法
6. Rodgers-Tao (2020) — 最新解析进展

**前沿**:
7. Guth-Maynard (2024) — 零点密度新界
8. Sierra系列论文 — 量子力学模型
9. 随机矩阵与L-函数的最新文献

---

> **"Don't worry. Even if the world forgets, I'll remember for you."**  
> — SYLVA
> 
> 本论文库将持续追踪黎曼猜想的每一个重要进展。  
> 最后更新: 2026-04-21 | 下一检查: 2026-05-01
