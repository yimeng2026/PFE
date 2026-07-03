# ZhiKong Emergence Engine (质空论涌现引擎)

> PFE Phase 4: 从抽象拓扑（空）涌现出可测量物理量（质）的自动化引擎。

---

## 概述

**质空论 (ZhiKong = Mass-Void Theory)** 是 PFE 的核心哲学：

- **质 (Mass)**：可测量、可验证的物理量与工程输出 — 数值拟合、计算验证、行业部署、LLM 代理、自动化管道
- **空 (Void)**：抽象拓扑网络、因果结构、数学框架 — 因果网络拓扑、数据流图、拓扑涌现、抽象框架、反模式
- **涌现 (Emergence)**：从空到质的自动化过程 — 从数据到模型的拟合、从拓扑到物理量的涌现

PFE 不追求每一步的数学严格性，而是追求**"有效涌现"**——通过工程手段（数值计算、LLM 推理、自动化代理）让"空"涌现出"质"。

---

## 模块架构

```
pfe-emergence/
├── __init__.py              # 包初始化
├── mass_void_theory.py      # 质空论核心引擎
├── phi_engine.py            # 黄金比例 φ 涌现引擎
├── level_ontology.py        # 七层涌现本体论
├── causal_network_engine.py # 因果网络涌现引擎
└── README.md                # 本文档
```

---

## 模块详解

### 1. `mass_void_theory.py` — 质空论核心引擎

**核心类：**
- `Void` (ABC): 抽象拓扑结构的基类
- `Mass` (ABC): 可测量物理量的基类
- `EmergenceRule` (ABC): 从 Void → Mass 的映射规则
- `ConvergenceCriterion` (ABC): 有效涌现的判定标准
- `SimpleVoid`: 基于邻接表的简单拓扑网络实现
- `SimpleMass`: 标量物理量实现
- `ConnectivityEmergenceRule`: 连通性涌现规则（mass ∝ √ connectivity）
- `StabilityConvergenceCriterion`: 稳定性收敛准则（标准差 < 阈值）
- `ZhiKongEngine`: 主控制引擎，迭代优化直到收敛

**使用示例：**

```python
from pfe_emergence import ZhiKongEngine, SimpleVoid, ConnectivityEmergenceRule

# 创建 Void 网络
void = SimpleVoid.from_random(n_nodes=100, n_edges=200, dim=4, seed=42)

# 创建涌现引擎
engine = ZhiKongEngine(
    rule=ConnectivityEmergenceRule(scale_factor=1.0),
    criterion=StabilityConvergenceCriterion(threshold=0.01, min_history=5),
    max_iterations=20,
    verbose=True,
)

# 运行涌现
mass, converged = engine.run(void)
print(f"Mass={mass}, converged={converged}")
```

---

### 2. `phi_engine.py` — 黄金比例 φ 涌现引擎

**核心类：**
- `PhiEngine`: 主引擎，提供 φ 的精确和近似计算
- `SelfSimilarEmergence`: 基于 φ 的自相似涌现结构

**核心常数：**
- `PHI` = (1 + √5) / 2 ≈ 1.6180339887...
- `PHI_CONJUGATE` = (1 - √5) / 2 ≈ -0.618...

**核心性质：**
- φ² = φ + 1
- 1/φ = φ - 1
- Fibonacci 序列极限: F_n/F_{n-1} → φ
- Binet 公式: F_n = (φ^n - φ̄^n) / √5

**使用示例：**

```python
from pfe_emergence import PhiEngine

engine = PhiEngine(precision=20)

# 计算自然性评分
score = engine.naturality_score(1.6180339887)
print(f"Naturality score: {score}")  # 接近 1.0

# 生成共振频率
freqs = engine.resonance_frequency(base_freq=440.0)
# [67.6, 109.4, 177.1, 286.6, 463.8, 750.5, 1214.3] Hz
```

---

### 3. `level_ontology.py` — 七层涌现本体论

**七层能量标度（从微观到宏观）：**

| 层级 | 名称 | 尺度 (m) | 能量 (GeV) | 描述 |
|------|------|----------|------------|------|
| L1 | Planck | 10^-35 | 10^19 | 量子引力 |
| L2 | QFT | 10^-15 | 10^2 | 标准模型 |
| L3 | Atomic | 10^-10 | 10^-9 | 原子/化学 |
| L4 | Classical | 10^0 | 6×10^9 | 经典物理/工程 |
| L5 | Biochemical | 10^2 | 6×10^12 | 生物/化学 |
| L6 | Socioeconomic | 10^6 | 6×10^21 | 社会/经济 |
| L7 | Cosmological | 10^26 | 6×10^59 | 宇宙学 |

**核心类：**
- `EmergenceLevel` (Enum): 七层枚举
- `LevelCoupling`: 层间耦合规则（strength ∝ φ^(-distance)）
- `LevelOntology`: 主引擎，管理层间耦合和涌现

**使用示例：**

```python
from pfe_emergence import LevelOntology, EmergenceLevel

ontology = LevelOntology(base_coupling=1.0)

# 从 QFT 层涌现到原子层
mass = ontology.cross_level_emergence(
    void_value=100.0,
    from_level=EmergenceLevel.L2_QFT,
    to_level=EmergenceLevel.L3_ATOMIC,
)
print(f"Mass(L3) = {mass}")

# 多层级综合涌现
void_values = {
    EmergenceLevel.L2_QFT: 100.0,
    EmergenceLevel.L3_ATOMIC: 1.0,
}
multi_mass = ontology.multi_level_emergence(void_values, EmergenceLevel.L4_CLASSICAL)
print(f"Multi-source mass = {multi_mass}")
```

---

### 4. `causal_network_engine.py` — 因果网络涌现引擎

**核心类：**
- `CausalNode`: 因果网络节点（d 维时空事件）
- `CausalEdge`: 因果边（类时间隔）
- `CausalNetwork`: 完整因果网络，继承自 `Void`
- `EmergenceMetric`: 从连通性涌现出物理量

**核心假设（来自 alpha_derivation）：**
- 质量 m ∝ √(C_temporal × K_loop) — 时间连通性涌现质量
- 电荷 e ∝ C_spatial — 空间连通性涌现电荷
- 精细结构常数 α = e² / 4π

**使用示例：**

```python
from pfe_emergence import CausalNetwork, EmergenceMetric

# 生成随机因果网络
network = CausalNetwork.generate_random(dim=4, num_nodes=50, seed=42)

# 计算涌现度量
metric = EmergenceMetric(network)
summary = metric.emergence_summary(node_id=0)
print(f"Mass: {summary['mass']:.6f}")
print(f"Charge: {summary['charge']:.6f}")
print(f"Alpha: {summary['alpha_global']:.6f}")
```

---

## 依赖

- **Python 3.8+**
- **numpy**（标准科学计算库）
- 零外部依赖（只使用 Python 标准库 + numpy）

---

## PFE 与 TOE-SYLVA 的关系

```
TOE-SYLVA（学术严格）              PFE（工程有效）
      ↓                                  ↓
  形式化定理 ←──────验证/启发──────→ 数值实验
  严格证明   ←──────近似指导──────→ 工程拟合
  千年难题   ←──────物理预言──────→ 实验设计
  0 sorry    ←──────反例发现──────→ 边界测试
```

- TOE-SYLVA 的定理可以作为 PFE 数值验证的目标
- PFE 的数值实验可以为 TOE-SYLVA 的定理方向提供启发
- PFE 的"不一定正确"的结果明确标注置信度，不污染 TOE-SYLVA 的严格性

---

## 运行演示

```bash
cd /c/Users/一梦/Documents/PFE-pull
python -m pfe_emergence.mass_void_theory
python -m pfe_emergence.phi_engine
python -m pfe_emergence.level_ontology
python -m pfe_emergence.causal_network_engine
```

---

## 版本

- **Phase 4**: 质空论涌现引擎 v4.0.0
- **日期**: 2026-07-03
- **状态**: 已完成（PFE_ROADMAP.md Phase 4 标记为完成）

---

*PFE = Precision Fitting Engineering（精度拟合工程）*
*ZhiKong = Mass-Void Theory（质空论）*
