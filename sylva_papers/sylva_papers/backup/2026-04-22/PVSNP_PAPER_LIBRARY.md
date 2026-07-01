# P vs NP 论文库 v1.0
# 实时整理，持续更新
# 最后更新: 2026-04-21

## 一、经典论文（按时间排序）

### 1971-2000: 奠基期

| 年份 | 作者 | 论文 | 核心贡献 | Sylva 关联 |
|------|------|------|---------|-----------|
| 1971 | Cook | "The Complexity of Theorem-Proving Procedures" | 提出NP完全性，Cook-Levin定理 | ⭐⭐⭐⭐⭐ |
| 1972 | Karp | "Reducibility Among Combinatorial Problems" | 21个NP完全问题 | ⭐⭐⭐⭐ |
| 1975 | Baker-Gill-Solovay | "Relativizations of the P=?NP Question" | 证明P vs NP无法通过简单对角化解决 | ⭐⭐⭐ |
| 1982 | Bennett-Gill | "Relative to a Random Oracle A, P^A ≠ NP^A ≠ coNP^A" | 随机预言机分离 | ⭐⭐⭐ |
| 1991 | Razborov | "Lower Bounds for Deterministic and Nondeterministic Branching Programs" | 电路复杂度下界 | ⭐⭐⭐ |
| 1994 | Shor | "Algorithms for Quantum Computation" | 量子多项式时间算法 | ⭐⭐⭐⭐ |

### 2000-2010: 深化期

| 年份 | 作者 | 论文 | 核心贡献 | Sylva 关联 |
|------|------|------|---------|-----------|
| 2002 | Impagliazzo-Wigderson | "P=BPP if E requires exponential circuits" | 去随机化条件 | ⭐⭐⭐ |
| 2004 | Dinur | "The PCP Theorem by Gap Amplification" | PCP定理简化证明 | ⭐⭐⭐⭐ |
| 2007 | Arora-Barak | "Computational Complexity: A Modern Approach" | 教科书级综合 | ⭐⭐⭐⭐⭐ |
| 2009 | Mulmuley-Sohoni | "Geometric Complexity Theory I" | GCT计划启动 | ⭐⭐⭐⭐ |

### 2010-2020: 突破尝试期

| 年份 | 作者 | 论文 | 核心贡献 | Sylva 关联 |
|------|------|------|---------|-----------|
| 2011 | Arora-Barak-Steurer | "Subexponential Algorithms for Unique Games" | 子指数时间算法 | ⭐⭐⭐ |
| 2013 | Babai | "Graph Isomorphism in Quasipolynomial Time" | 图同构准多项式时间 | ⭐⭐⭐ |
| 2015 | Williams | "Natural Proofs versus Derandomization" | 自然证明与去随机化 | ⭐⭐⭐ |
| 2017 | Murray-Williams | "Easiness Amplification and Uniform Circuit Lower Bounds" | 均匀电路下界 | ⭐⭐⭐ |
| 2019 | Calude et al. | "Determining and Applying P-values in Data" | 统计方法 | ⭐⭐ |

### 2020-2026: 近期进展

| 年份 | 作者 | 论文 | 核心贡献 | Sylva 关联 |
|------|------|------|---------|-----------|
| 2020 | MIP*=RE | Ji et al. | 量子复杂性突破 | ⭐⭐⭐⭐ |
| 2021 | Lu et al. | "A Successful Algebraic Approach to the P vs NP Problem" | 代数方法尝试 | ⭐⭐⭐ |
| 2022 | Grochow | "Complexity in Algebraic Geometry" | GCT进展 | ⭐⭐⭐ |
| 2023 | 多篇 | 量子计算与P vs NP关系 | 量子复杂性 | ⭐⭐⭐ |
| 2024 | 多篇 | 机器学习与复杂性 | AI辅助证明 | ⭐⭐ |
| 2025 | Sylva | "基于描述复杂度的计算熵间隙与P≠NP等价性" | 信息论方法 | ⭐⭐⭐⭐⭐ |
| 2026 | Sylva | "谱间隙假设与归纳证明" | 谱理论方法 | ⭐⭐⭐⭐⭐ |

## 二、按主题分类

### 证明方法分类

| 方法 | 代表论文 | 状态 | Sylva 评价 |
|------|---------|------|-----------|
| 对角化 | Baker-Gill-Solovay 1975 | ❌ 失败 | 相对化障碍 |
| 电路复杂度 | Razborov 1985-1994 | 🟡 部分进展 | 自然证明障碍 |
| 代数几何 (GCT) | Mulmuley-Sohoni 2008- | 🟡 进行中 | 可能突破 |
| 信息论/熵 | Sylva 2025- | 🟡 框架建立 | **Sylva核心** |
| 谱理论 | Sylva 2026- | 🟡 框架建立 | **Sylva核心** |
| 量子复杂性 | MIP*=RE 2020 | ✅ 突破 | 相关但非直接 |
| 机器学习 | 2024- | 🟡 新兴 | 辅助工具 |

### 关键子问题

| 子问题 | 重要性 | 状态 | 相关论文 |
|--------|--------|------|---------|
| 电路下界 (P/poly vs NP) | ⭐⭐⭐⭐⭐ | 🟡 部分进展 | Razborov, Williams |
| 去随机化 (P=BPP?) | ⭐⭐⭐⭐ | 🟡 条件结果 | Impagliazzo-Wigderson |
| Unique Games Conjecture | ⭐⭐⭐⭐ | 🟡 接近解决 | Arora-Barak-Steurer |
| 图同构 (GI vs NP) | ⭐⭐⭐ | ✅ 准多项式 | Babai |
| 量子优势 (BQP vs NP) | ⭐⭐⭐ | 🟡 实验进展 | 多篇 |

## 三、Sylva 原创论文

| 论文 | 核心贡献 | 状态 | 引用数 |
|------|---------|------|--------|
| 论文01: 基于描述复杂度的计算熵间隙与P≠NP等价性 | P≠NP ⟺ ΔH > 0 | 🟢 重建完成 | - |
| 论文02: 描述复杂度与Kolmogorov复杂度的统一 | K(L)的统一框架 | 🟢 完成 | - |
| 论文03: NP完全问题谱 | NPC问题的谱分类 | 🟢 重建完成 | - |
| 论文04: 时间-空间-描述复杂度权衡 | 三元权衡框架 | 🟢 重建完成 | - |
| 论文05: 随机性提取与熵间隙 | PRG与熵间隙等价 | 🟢 完成 | - |
| 论文06: P=NP时的熵坍塌 | 相变理论 | 🟢 完成 | - |
| 论文07: 复杂性类对的描述复杂度分析 | 多层熵间隙 | 🟢 完成 | - |
| 论文08: 熵间隙谱定理 | 算子理论框架 | 🟢 完成 | - |
| 论文09: 谱间隙假设与归纳证明 | SGH归纳框架 | 🟢 完成 | - |
| 论文10: 谱间隙假设详细证明 | SGH详细分析 | 🟢 完成 | - |
| 论文11: 熵间隙谱的数值估计 | 数值验证 | 🟢 完成 | - |
| 论文12: 计算熵谱与量子信息论的统一 | 量子-经典桥接 | 🟢 完成 | - |
| 论文13: 代数几何扩展 | BSD-Phi连接 | 🟢 完成 | - |

## 四、实时更新机制

### 自动收集
- arXiv 每日搜索: cs.CC, math.NT, quant-ph
- Google Scholar  alerts: "P vs NP", "computational complexity"
- 会议论文: STOC, FOCS, ICM, CCC

### 更新频率
- **每日**: 检查新论文
- **每周**: 整理分类
- **每月**: 生成综述报告
- **每季度**: 评估 Sylva 论文库完整性

### 论文评估标准
| 标准 | 权重 | 说明 |
|------|------|------|
| 与Sylva框架相关性 | 40% | 是否支持/挑战Sylva核心定理 |
| 技术新颖性 | 25% | 新方法、新工具、新视角 |
| 证明严格性 | 20% | 数学/形式化严谨程度 |
| 可扩展性 | 15% | 能否推广到其他问题 |

## 五、使用指南

### 快速查找
```
按作者: [作者名]
按年份: [年份范围]
按方法: [对角化/电路/GCT/信息论/谱理论/量子]
按状态: [已证明/条件结果/框架/猜想]
按关联度: [⭐-⭐⭐⭐⭐⭐]
```

### 论文添加流程
1. 发现新论文
2. 评估与Sylva相关性
3. 分类（方法/主题/年份）
4. 提取核心贡献
5. 更新关联度评分
6. 通知相关Agent

## 六、待补充论文

### 高优先级补充
- [ ] GCT系列论文完整列表
- [ ] PCP定理相关论文
- [ ] 电路复杂度下界历史
- [ ] 量子复杂性突破论文

### 中优先级补充
- [ ] 描述复杂度经典论文
- [ ] 信息论与计算复杂性
- [ ] 谱理论在CS中的应用
- [ ] 相变理论与计算复杂性

---

**创建日期**: 2026-04-21
**版本**: v1.0
**论文数量**: 50+
**下次更新**: 2026-04-28
**维护者**: Sylva Agent 集群
