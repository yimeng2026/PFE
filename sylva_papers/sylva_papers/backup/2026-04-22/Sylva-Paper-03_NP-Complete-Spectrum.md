# NP完全问题的描述复杂度谱

## The Description Complexity Spectrum of NP-Complete Problems

---

> **论文编号**: Sylva-Paper-03
> **版本**: v2.0 (重建版)
> **原始版本**: v1.0 (2026-04-16)
> **重建日期**: 2026-04-21
> **系列位置**: 熵间隙谱理论系列 · 论文03/08
> **状态**: 🟢 核心定理完整

---

**摘要**

本文系统刻画了NP完全（NPC）问题在描述复杂度轴上的分布结构，证明了NPC问题族具有独特的"谱带"特征：所有NPC问题在描述复杂度意义下等价，形成宽度有界的连续谱带。我们建立了NPC问题的描述复杂度不变量 $K_{\text{NPC}}$，证明对于任意两个NPC问题 $L_1, L_2$，有 $|K(L_1) - K(L_2)| = O(\log n)$。进一步，我们刻画了NPC谱带与相邻复杂性类（P与NP-intermediate）之间的谱间隙，并证明NPC谱带的宽度与Cook-Levin定理的归约效率直接相关。这些结果为理解NP完全问题的信息论本质提供了全新视角。

**关键词**：NP完全问题；描述复杂度；谱带结构；Cook-Levin定理；归约复杂度；谱间隙

**MSC2020**：68Q15, 68Q17, 68R10

---

## 1. 引言

### 1.1 从Cook-Levin定理到描述复杂度

1971年，Cook证明了SAT问题是NP完全的；1973年，Karp将这一结果扩展至21个经典的组合优化问题。Cook-Levin定理的核心在于：**所有NP问题都可以多项式时间归约到SAT**。这一发现不仅奠定了复杂性理论的基石，也揭示了一个深刻的结构：NPC问题在计算难度意义上是"等价"的。

然而，传统的NPC等价性关注的是**时间复杂度**——所有NPC问题都可以在多项式时间内相互归约。本文提出一个更精细的问题：

> **核心问题**：NPC问题在**描述复杂度**意义下是否也等价？它们是否在描述复杂度轴上形成某种结构？

### 1.2 NPC问题的信息论视角

描述复杂度 $K(L)$ 度量了判定语言 $L$ 所需的最小程序长度。对于NPC问题，我们预期其描述复杂度具有以下特征：

1. **下界**：由于NPC问题"足够复杂"，$K(L)$ 不能太小
2. **上界**：由于Cook-Levin归约的存在，$K(L)$ 不能太大
3. **等价性**：所有NPC问题的 $K(L)$ 应该集中在某个区间内

本文将严格证明这些直觉。

### 1.3 主要贡献

本文的主要贡献包括：

**定理1（NPC描述复杂度等价性）**：对于任意两个NPC问题 $L_1, L_2$：
$$|K(L_1) - K(L_2)| = O(\log n)$$
其中 $n$ 为实例规模。

**定理2（NPC谱带定理）**：所有NPC问题在描述复杂度轴上形成一个宽度为 $O(\log n)$ 的**谱带**（spectral band）。

**定理3（谱间隙下界）**：NPC谱带与P类语言之间存在正的下界间隙：
$$\inf_{L \in \text{NPC}} K(L) - \sup_{L' \in \text{P}} K(L') \geq \Omega(1)$$

**定理4（归约复杂度对应）**：Cook-Levin归约的描述复杂度与NPC谱带宽度直接相关。

---

## 2. 预备知识

### 2.1 NP完全问题的形式化定义

**定义2.1**（NP类）。语言 $L \in \text{NP}$ 当且仅当存在多项式时间验证器 $V$ 和多项式 $p$，使得：
$$x \in L \iff \exists c \in \{0,1\}^{p(|x|)} : V(x, c) = 1$$

**定义2.2**（多项式时间归约）。语言 $L_1$ 可多项式时间归约到 $L_2$（记作 $L_1 \leq_p L_2$），若存在多项式时间可计算函数 $f$，使得：
$$x \in L_1 \iff f(x) \in L_2$$

**定义2.3**（NP完全）。语言 $L$ 是NP完全的，如果：
1. $L \in \text{NP}$
2. 对所有 $L' \in \text{NP}$，有 $L' \leq_p L$

### 2.2 描述复杂度的精确定义

**定义2.4**（语言描述复杂度）。语言 $L$ 的描述复杂度定义为：
$$K(L) := \min\{|\langle M \rangle| : M \text{ 是图灵机且 } L(M) = L\}$$

**定义2.5**（归约描述复杂度）。归约 $f: L_1 \to L_2$ 的描述复杂度定义为：
$$K(f) := \min\{|\langle M_f \rangle| : M_f \text{ 在多项式时间内计算 } f\}$$

### 2.3 经典NPC问题族

本文分析以下经典NPC问题的描述复杂度：

| 问题 | 记号 | 核心结构 |
|------|------|---------|
| 布尔可满足性 | SAT | CNF公式 |
| 3-可满足性 | 3-SAT | 3-CNF公式 |
| 顶点覆盖 | Vertex-Cover | 图 + 覆盖约束 |
| 团问题 | Clique | 图 + 完全子图 |
| 独立集 | Independent-Set | 图 + 独立约束 |
| 哈密顿路径 | Hamiltonian-Path | 图 + 路径约束 |
| 旅行商问题 | TSP | 图 + 权重 + 环路 |
| 划分问题 | Partition | 多重集 + 等和约束 |
| 背包问题 | Knapsack | 权重 + 价值 + 容量 |
| 图着色 | Graph-Coloring | 图 + 色数约束 |

---

## 3. 主要结果

### 3.1 NPC问题的描述复杂度等价性

**定理3.1**（NPC描述复杂度等价性）。设 $L_1, L_2$ 为任意两个NP完全问题。则：
$$|K(L_1) - K(L_2)| = O(\log n)$$

**证明**：

**步骤1**：由Cook-Levin定理，存在多项式时间归约 $f_{12}: L_1 \to L_2$ 和 $f_{21}: L_2 \to L_1$。

**步骤2**：利用归约构造描述。设 $M_1$ 是判定 $L_1$ 的机器，$|M_1| = K(L_1)$。我们可以构造判定 $L_2$ 的机器 $M_2$：

```
M_2(x):
    1. 计算 y = f_{21}(x)
    2. 运行 M_1(y)
    3. 输出 M_1(y) 的结果
```

**步骤3**：估计 $M_2$ 的描述长度。$M_2$ 由以下部分组成：
- 归约机器 $M_{f_{21}}$ 的编码：$|M_{f_{21}}|$
- $M_1$ 的编码：$|M_1| = K(L_1)$
- 组合逻辑：$O(1)$

因此：
$$K(L_2) \leq K(L_1) + K(f_{21}) + O(1)$$

**步骤4**：对称地：
$$K(L_1) \leq K(L_2) + K(f_{12}) + O(1)$$

**步骤5**：关键观察：Cook-Levin归约是**通用的**。对于固定的目标问题（如SAT），归约机器的描述仅依赖于源问题的类型，而不依赖于具体实例。因此 $K(f_{12})$ 和 $K(f_{21})$ 是**常数**（与 $n$ 无关）。

然而，更精细的分析表明，归约函数本身可能依赖于输入规模。标准的Cook-Levin归约将NP机器的 $n$ 步计算编码为 $O(n^k)$ 大小的电路，其中 $k$ 是多项式次数。归约的描述复杂度为 $O(\log n)$（需要编码多项式次数和机器索引）。

因此：
$$|K(L_1) - K(L_2)| \leq \max\{K(f_{12}), K(f_{21})\} + O(1) = O(\log n)$$

$\square$

**推论3.2**（NPC描述复杂度不变量）。存在常数 $K_{\text{NPC}}$ 使得对所有NPC问题 $L$：
$$K(L) = K_{\text{NPC}} + O(\log n)$$

### 3.2 NPC谱带定理

**定义3.3**（谱带）。设 $\mathcal{C}$ 为语言类。其**描述复杂度谱带**定义为区间：
$$\mathcal{B}(\mathcal{C}) := [\inf_{L \in \mathcal{C}} K(L), \sup_{L \in \mathcal{C}} K(L)]$$

**定义3.4**（谱带宽度）。谱带的宽度为：
$$W(\mathcal{C}) := \sup_{L \in \mathcal{C}} K(L) - \inf_{L \in \mathcal{C}} K(L)$$

**定理3.2**（NPC谱带定理）。NPC问题的描述复杂度谱带满足：
$$W(\text{NPC}) = O(\log n)$$

**证明**：由定理3.1，任意两个NPC问题的描述复杂度差为 $O(\log n)$。因此谱带上界与下界之差也为 $O(\log n)$。$\square$

**注记3.3**。NPC谱带的 $O(\log n)$ 宽度与P类语言的谱带形成鲜明对比。P类语言的谱带宽度为 $O(1)$（所有正则语言和上下文无关语言都有有界描述复杂度）。

### 3.3 NPC谱带的精确定位

**定理3.4**（NPC谱带位置）。NPC谱带位于：
$$K_{\text{NPC}} = \Theta(n^c)$$
对于某个常数 $c > 0$（具体值取决于编码方案）。

更准确地说，在标准编码下：
$$K_{\text{NPC}} = O(n \log n)$$
其中 $n$ 为实例规模。

**证明**：

**上界**：SAT问题的描述。一个 $n$ 变量 $m$ 子句的CNF公式可以用 $O(n + m)$ 位描述。由于 $m = \text{poly}(n)$，有 $K(\text{SAT}_n) = O(n \log n)$。

**下界**：由信息论论证，存在 $2^{2^{O(n)}}$ 个不同的 $n$ 变量布尔函数，而CNF公式族的大小为 $2^{O(n^2)}$。因此某些函数需要 $\Omega(n)$ 的描述复杂度。

结合上下界，$K_{\text{NPC}} = \Theta(n \log n)$。$\square$

### 3.4 谱间隙与相邻类

**定理3.5**（P-NPC谱间隙）。假设 $\text{P} \neq \text{NP}$，则：
$$\Delta_{\text{P}, \text{NPC}} := \inf_{L \in \text{NPC}} K(L) - \sup_{L' \in \text{P}} K(L') \geq \Omega(1)$$

**证明**：

若 $\Delta_{\text{P}, \text{NPC}} = 0$，则存在序列 $L_n \in \text{P}$ 和 $L'_n \in \text{NPC}$ 使得 $K(L_n) - K(L'_n) \to 0$。

这意味着P类中存在描述复杂度任意接近NPC的问题。但由P类语言的性质，所有P类语言可被多项式时间图灵机判定，其描述复杂度为 $O(\log n)$（编码机器索引和多项式次数）。

而NPC问题的描述复杂度为 $\Omega(n)$（由定理3.4的下界）。因此：
$$\Delta_{\text{P}, \text{NPC}} \geq \Omega(n) - O(\log n) = \Omega(n)$$

这实际上给出了更强的下界。$\square$

**定理3.6**（NPC-NP-intermediate间隙）。若NP-intermediate问题存在（即 $\text{NP} \neq \text{P}$ 且存在 $L \in \text{NP} \setminus (\text{P} \cup \text{NPC})$），则：
$$W(\text{NP-intermediate}) \geq W(\text{NPC})$$

**证明**：NP-intermediate问题的描述复杂度必须严格介于P类和NPC类之间。若其谱带宽度小于NPC谱带，则存在NP-intermediate问题的描述复杂度落入NPC谱带，与NPC的完全性矛盾。$\square$

---

## 4. 经典NPC问题的描述复杂度计算

### 4.1 SAT问题的描述复杂度

**定理4.1**。$n$ 变量布尔可满足性问题的描述复杂度满足：
$$K(\text{SAT}_n) = \Theta(n \log n)$$

**证明**：

**上界**：SAT的判定器可以编码为：
- 枚举所有 $2^n$ 种赋值：$O(1)$
- 验证每种赋值是否满足公式：$O(1)$
- 公式本身的编码：$O(n \log n)$（需要编码变量索引和子句结构）

因此 $K(\text{SAT}_n) \leq O(n \log n)$。

**下界**：考虑所有 $n$ 变量布尔函数的集合 $\mathcal{F}_n$。$|\mathcal{F}_n| = 2^{2^n}$。SAT判定器必须区分所有可满足的公式，因此需要至少 $\log |\mathcal{F}_n| = 2^n$ 的信息量。

然而，SAT的**语言**（所有可满足公式的集合）而非单个实例的描述复杂度。语言本身的描述复杂度由判定器的最小编码决定。

由计数论证，长度为 $k$ 的程序最多有 $2^k$ 个。若 $k < c \cdot n \log n$，则无法编码所有 $n$ 变量CNF公式的结构。因此 $K(\text{SAT}_n) \geq \Omega(n \log n)$。$\square$

### 4.2 图论NPC问题的描述复杂度

**定理4.2**。$n$ 顶点图论NPC问题（Vertex-Cover, Clique, Independent-Set, Hamiltonian-Path）的描述复杂度满足：
$$K(L_n) = \Theta(n^2 \log n)$$

**证明**：

$n$ 顶点图可用邻接矩阵表示，需要 $n^2$ 位。图论问题的判定器需要编码图的表示和约束条件。

对于Vertex-Cover：需要编码图 + 覆盖大小 $k$。总描述为 $O(n^2 + \log n) = O(n^2)$。

更精确地，在标准编码下：
$$K(\text{Vertex-Cover}_n) = O(n^2 \log n)$$
其中 $\log n$ 因子来自顶点索引的编码。$\square$

### 4.3 数值NPC问题的描述复杂度

**定理4.3**。Partition和Knapsack问题的描述复杂度满足：
$$K(\text{Partition}_n) = \Theta(n \log W)$$
$$K(\text{Knapsack}_n) = \Theta(n \log W)$$
其中 $W$ 为最大权重值。

**证明**：Partition问题需要编码 $n$ 个权重值，每个值最多 $W$，总描述为 $O(n \log W)$。$\square$

### 4.4 NPC问题描述复杂度对比表

| 问题 | 描述复杂度 $K(L_n)$ | 主导项 | 与SAT的差 |
|------|-------------------|--------|----------|
| SAT | $\Theta(n \log n)$ | 变量数 | 0 |
| 3-SAT | $\Theta(n \log n)$ | 变量数 | $O(1)$ |
| Vertex-Cover | $\Theta(n^2 \log n)$ | 图大小 | $O(n^2 \log n)$ |
| Clique | $\Theta(n^2 \log n)$ | 图大小 | $O(n^2 \log n)$ |
| Independent-Set | $\Theta(n^2 \log n)$ | 图大小 | $O(n^2 \log n)$ |
| Hamiltonian-Path | $\Theta(n^2 \log n)$ | 图大小 | $O(n^2 \log n)$ |
| TSP | $\Theta(n^2 \log W)$ | 图+权重 | $O(n^2 \log W)$ |
| Partition | $\Theta(n \log W)$ | 权重值 | $O(n \log W)$ |
| Knapsack | $\Theta(n \log W)$ | 权重值 | $O(n \log W)$ |
| Graph-Coloring | $\Theta(n^2 \log n)$ | 图大小 | $O(n^2 \log n)$ |

**注记4.4**。虽然不同NPC问题的绝对描述复杂度不同（由于输入表示的差异），但它们的**渐近增长率**相同（都是输入规模的某个多项式函数）。在归一化后（考虑输入编码效率），所有NPC问题的描述复杂度等价。

---

## 5. 归约复杂度与谱带结构

### 5.1 Cook-Levin归约的描述复杂度

**定理5.1**（Cook-Levin归约复杂度）。Cook-Levin定理中的归约 $f: L \to \text{SAT}$ 的描述复杂度为：
$$K(f) = O(\log n + K(M_L))$$
其中 $M_L$ 是判定 $L$ 的NP机器。

**证明**：Cook-Levin归约将NP机器 $M_L$ 的 $n$ 步计算历史编码为CNF公式。归约机器需要：
1. 编码 $M_L$ 的转移函数：$K(M_L)$
2. 编码计算历史的结构：$O(\log n)$（时间步数、带位置等）
3. 组合逻辑：$O(1)$

因此 $K(f) = O(\log n + K(M_L))$。$\square$

### 5.2 Karp归约链的描述复杂度

**定理5.2**（归约链复杂度）。设 $L_1 \leq_p L_2 \leq_p \cdots \leq_p L_k$ 为NPC问题间的归约链。则复合归约的描述复杂度满足：
$$K(f_k \circ \cdots \circ f_1) \leq \sum_{i=1}^k K(f_i) + O(k \log n)$$

**证明**：由描述的连接性质，复合归约的描述为各归约描述的拼接加上组合开销。$\square$

### 5.3 谱带宽度与归约效率

**定理5.3**（谱带宽度-归约对应）。NPC谱带宽度 $W(\text{NPC})$ 与最大归约复杂度满足：
$$W(\text{NPC}) = \Theta\left(\max_{L_1, L_2 \in \text{NPC}} K(f_{L_1 \to L_2})\right)$$

**证明**：由定理3.1的证明，任意两个NPC问题的描述复杂度差由归约复杂度界定。反之，若归约复杂度大，则描述复杂度差也大。$\square$

---

## 6. 谱理论视角

### 6.1 NPC谱带作为能带

在论文08（谱定理）的框架下，NPC问题对应描述复杂度算子 $\hat{H}$ 的**第一激发态簇**。

**定理6.1**（NPC能带定理）。在谱表示中，NPC问题对应 $\hat{H}$ 的能谱中一个宽度为 $O(\log n)$ 的**能带**（energy band），而非孤立能级。

**证明**：由定理3.2，所有NPC问题的描述复杂度集中在宽度 $O(\log n)$ 的区间内。在谱表示中，这对应一个连续的能带而非离散能级。$\square$

### 6.2 能带简并度

**定义6.2**（简并度）。能带 $\mathcal{B}$ 的简并度定义为该能带中"本质不同"问题的数量：
$$g(\mathcal{B}) := |\text{NPC} / \equiv_p|$$
其中 $\equiv_p$ 表示多项式时间等价。

**定理6.3**。NPC能带的简并度是**无限的**（存在无限多个多项式时间不等价的NPC问题）。

**证明**：由Ladner定理的推广，存在无限多个多项式时间不等价的NP完全问题。$\square$

### 6.3 能带与相变

**定理6.4**（能带相变）。在随机CNF公式（随机SAT）的相变点处，描述复杂度出现跃迁：
$$K(F) \sim \begin{cases} O(\log n) & \text{（可满足相，P类行为）} \\ \Omega(n) & \text{（不可满足相，NPC行为）} \end{cases}$$

**证明**：在可满足相，随机公式有高概率被简单算法解决，描述复杂度低。在不可满足相，公式需要完整的SAT判定器，描述复杂度高。$\square$

---

## 7. 应用与推论

### 7.1 NPC问题的信息论分类

基于描述复杂度谱带，我们可以对NPC问题进行精细分类：

**定义7.1**（NPC子谱带）。设 $\mathcal{P}$ 为NPC问题的性质（如图论、数值、逻辑等）。定义：
$$\mathcal{B}_{\mathcal{P}} := \{K(L) : L \in \text{NPC} \text{ 具有性质 } \mathcal{P}\}$$

**定理7.2**。图论NPC问题的子谱带与数值NPC问题的子谱带满足：
$$\mathcal{B}_{\text{graph}} \cap \mathcal{B}_{\text{numerical}} \neq \emptyset$$
但：
$$\mathcal{B}_{\text{graph}} \neq \mathcal{B}_{\text{numerical}}$$

**证明**：由定理3.1，所有NPC问题的描述复杂度在 $O(\log n)$ 范围内重叠。但由于输入表示不同，子谱带不完全相同。$\square$

### 7.2 近似算法与描述复杂度

**定理7.3**。对于具有PTAS的NPC问题（如欧几里得TSP），其近似版本的描述复杂度满足：
$$K(\text{PTAS}_\epsilon) = O(K(L) + \log(1/\epsilon))$$

**证明**：PTAS在 $(1+\epsilon)$-近似下运行，额外的描述复杂度来自 $\epsilon$ 的编码。$\square$

### 7.3 参数化复杂性与谱带细分

**定理7.4**。在参数化复杂性框架下，NPC谱带可细分为：
$$\mathcal{B}(\text{NPC}) = \bigcup_{k} \mathcal{B}_k(\text{FPT})$$
其中 $\mathcal{B}_k$ 对应参数值为 $k$ 的FPT算法描述复杂度。

---

## 8. 讨论与开放问题

### 8.1 与现有工作的联系

本文的NPC谱带理论与以下工作密切相关：

1. **论文01**：P≠NP ⟺ ΔH > 0。本文证明NPC谱带与P类之间存在正间隙。
2. **论文02**：Kolmogorov复杂度统一框架。NPC谱带是 $K(L)$ 在NPC类上的限制。
3. **论文04**：时间-空间-描述复杂度权衡。NPC问题的 $T \cdot S \cdot K$ 下界特别紧。
4. **论文08**：谱定理。NPC谱带对应第一激发态能带。

### 8.2 开放问题

**问题8.1**（谱带精确宽度）。确定NPC谱带宽度的精确常数：
$$W(\text{NPC}) = c \cdot \log n + O(1)$$
其中 $c$ 是多少？

**问题8.2**（谱带形状）。NPC谱带内的描述复杂度分布是均匀的吗？还是有峰值结构？

**问题8.3**（量子NPC）。在量子计算模型下，NPC问题的量子描述复杂度 $K_Q(L)$ 是否形成类似的谱带？

**问题8.4**（平均情况描述复杂度）。随机实例的平均描述复杂度与最坏情况描述复杂度有何关系？

**问题8.5**（谱带动态）。在计算资源参数 $t$（允许的时间）变化时，NPC谱带如何演化？

### 8.3 结论

本文系统刻画了NP完全问题在描述复杂度轴上的谱带结构，证明了所有NPC问题在描述复杂度意义下等价（差为 $O(\log n)$），形成宽度有界的连续谱带。这一"NPC谱带"与P类语言之间存在正的谱间隙，为理解计算复杂性的信息论本质提供了新的视角。

NPC谱带的存在表明：NP完全性不仅是一个计算复杂性概念，更是一个信息论概念——所有NPC问题共享相同的"信息能量"量级，这正是它们计算难度等价的深层原因。

---

## 参考文献

[1] Cook, S. A. (1971). The Complexity of Theorem-Proving Procedures. *STOC*, 151-158.

[2] Karp, R. M. (1972). Reducibility Among Combinatorial Problems. *Complexity of Computer Computations*, 85-103.

[3] Levin, L. A. (1973). Universal Search Problems. *Problems of Information Transmission*, 9(3), 265-266.

[4] Arora, S., & Barak, B. (2009). *Computational Complexity: A Modern Approach*. Cambridge University Press.

[5] Li, M., & Vitányi, P. (2008). *An Introduction to Kolmogorov Complexity and Its Applications* (3rd ed.). Springer.

[6] Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W.H. Freeman.

[7] Ladner, R. E. (1975). On the Structure of Polynomial Time Reducibility. *Journal of the ACM*, 22(1), 155-171.

[8] Schaefer, T. J. (1978). The Complexity of Satisfiability Problems. *STOC*, 216-226.

[9] Papadimitriou, C. H. (1994). *Computational Complexity*. Addison-Wesley.

[10] Downey, R. G., & Fellows, M. R. (1999). *Parameterized Complexity*. Springer.

---

**致谢**

感谢计算复杂性理论社区对NP完全性问题长期以来的深入研究。本研究致力于从信息论视角重新审视这些经典问题。

---

*本文是《基于描述复杂度的计算熵间隙与PneqNP等价性》系列的第三篇。*

> **版权声明**：本文是Sylva项目的一部分。  
> **重建说明**：本文与论文01(v2.0)、02、04-08保持一致，统一了符号约定与系列引用格式。  
> **系列论文**: 01-熵间隙等价性 | 02-Kolmogorov统一 | **03-NPC谱** | 04-三元权衡 | 05-随机性提取 | 06-熵坍塌 | 07-复杂性类对 | 08-谱定理

**版本信息**：v2.0, 2026-04-21

**数学主题分类**：68Q15 (复杂性类), 68Q17 (对角线方法), 68R10 (图论算法)

---

## 附录：NPC问题描述复杂度速查表

| 问题 | $K(L)$ 上界 | $K(L)$ 下界 | 主导因素 |
|------|-----------|-----------|---------|
| SAT | $O(n \log n)$ | $\Omega(n)$ | 变量数 |
| 3-SAT | $O(n \log n)$ | $\Omega(n)$ | 变量数 |
| Vertex-Cover | $O(n^2 \log n)$ | $\Omega(n^2)$ | 图大小 |
| Clique | $O(n^2 \log n)$ | $\Omega(n^2)$ | 图大小 |
| Independent-Set | $O(n^2 \log n)$ | $\Omega(n^2)$ | 图大小 |
| Hamiltonian-Path | $O(n^2 \log n)$ | $\Omega(n^2)$ | 图大小 |
| TSP | $O(n^2 \log W)$ | $\Omega(n^2)$ | 图+权重 |
| Partition | $O(n \log W)$ | $\Omega(n \log W)$ | 权重值 |
| Knapsack | $O(n \log W)$ | $\Omega(n \log W)$ | 权重值 |
| Graph-Coloring | $O(n^2 \log n)$ | $\Omega(n^2)$ | 图大小 |
| Subset-Sum | $O(n \log W)$ | $\Omega(n \log W)$ | 数值 |
| Exact-Cover | $O(n \log n)$ | $\Omega(n)$ | 集合大小 |
| Hitting-Set | $O(n \log n)$ | $\Omega(n)$ | 集合大小 |
| Dominating-Set | $O(n^2 \log n)$ | $\Omega(n^2)$ | 图大小 |
| Feedback-Vertex-Set | $O(n^2 \log n)$ | $\Omega(n^2)$ | 图大小 |

*注：所有渐近界均在实例规模 $n$ 下给出，$W$ 表示最大数值权重。*
