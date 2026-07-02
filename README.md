# PFE — Precision Fitting Engineering

> **质空论工程原型**：从抽象拓扑（空）涌现物理可测量（质）的精度拟合系统。
> 
> 与 [TOE-SYLVA](https://github.com/yimeng2026/TOE-SYLVA) 的关系：SYLVA 是学术总纲（严格形式化），PFE 是工程应用（有效涌现）。

---

## 工程定位

| 维度 | TOE-SYLVA（学术） | PFE（工程） |
|------|------------------|------------|
| **正确性标准** | Lean 4 可编译，数学严格 | 有效即可，数值近似、启发式、LLM 推理均可 |
| **核心方法** | 形式化证明（theorem/lemma） | 数值验证、计算模拟、自动化代理、工程部署 |
| **输出形式** | `.lean` 证明 + 学术论文 | `.py` 计算脚本 + `.js` 自动化管道 + 行业部署方案 |
| **失败容忍** | 0 容忍（编译失败 = 不可接受） | 高容忍（误差 1e-6 可接受，启发式失败可迭代） |
| **千年难题** | 公理化/定理化，诚实标记 | 数值近似、物理模拟、实验预言、工程启发 |

**PFE 的核心哲学**：不追求每一步的数学严格性，而是追求**有效涌现**——通过工程手段（数值计算、LLM 推理、自动化代理）让"空"（抽象框架）涌现出"质"（可验证的物理预言和工程解决方案）。

---

## 目录结构

```
PFE/
├── PFE_MANIFESTO.md              # 质空论工程原型完整辨析
├── README.md                     # 本文件
├── sylva-release/               # 引用 TOE-SYLVA 核心形式化（只读引用，不直接修改）
│   └── README.md                # 指向 TOE-SYLVA 的引用说明
├── sagemath_verification/        # 数值计算引擎（SageMath/Python）
│   ├── elliptic_curve_reduction.py
│   ├── dynamical_system_factor_detection.py
│   ├── rank_verification.py
│   └── unified_verifier.py
├── alpha_derivation/             # 精细结构常数因果网络涌现推导
│   ├── 00_final_report.md
│   ├── 01_causal_network_simulation.py
│   ├── 02_fast_simulation.py
│   └── ...
├── toe_framework/               # 物理理论计算沙盒（80+ 理论框架）
│   ├── 01_experimental_verification.md
│   ├── 05_mathematical_foundations.md
│   └── ...
├── pfe-pipelines/               # 端到端自动化管道（新建）
├── pfe-agents/                  # 自主研究代理集群（新建）
├── sylva_agents/                # 20 代理集群历史档案
├── sylva_papers/                # 工程预印本与实验报告
├── sylva_academic/              # 学术资源（引用 TOE-SYLVA）
├── sylva_complete/              # 完整历史档案
└── sylva_formalization/         # 形式化历史（引用 TOE-SYLVA）
```

---

## 核心工程模块

### 1. 数值计算引擎 `sagemath_verification/`

基于 SageMath/Python 的数值验证工具，验证 TOE-SYLVA 形式化中的算法：

- **椭圆曲线约化判定**：`elliptic_curve_reduction.py`
- **动力系统因子检测**：`dynamical_system_factor_detection.py`
- **秩计算验证**：`rank_verification.py`
- **统一验证框架**：`unified_verifier.py`

### 2. 因果网络涌现 `alpha_derivation/`

质空论的核心实践：从因果网络拓扑连通性涌现电荷。

- 4 维因果网络模拟给出 α ≈ 0.0073-0.008（与 1/137 同数量级）
- 维度预测：α(d) 随维度增加单调递减，4 维处于"临界窗口"
- 拓扑修正：S³ vs T³ 对连通性分布有不同约束

### 3. 物理理论计算沙盒 `toe_framework/`

80+ 个物理理论框架的计算探索（不要求严格证明，要求有效计算）：

- 实验验证框架
- 理论修正计算
- QCD 涌现模拟
- 暗物质/暗能量参数扫描
- 电弱统一计算
- 量子引力近似
- 超对称参数空间
- ...

### 4. 自动化管道 `pfe-pipelines/`（新建）

端到端自动化工程管道：

- 数据注入 → 数值计算 → 结果验证 → 报告生成
- 与千界花园 LLM 后端集成，自动分析 TOE-SYLVA 的 sorry 并提供工程启发
- 行业部署模板自动生成

### 5. 自主代理 `pfe-agents/`（新建）

基于千界花园 LLM 集成（Zhipu GLM-5.1）的自主研究代理：

- 自动解析 TOE-SYLVA 的 Lean 代码，提取开放问题
- LLM 生成工程近似策略
- 数值验证代理自动执行 SageMath 脚本
- 结果评估代理判断"有效涌现"质量

---

## PFE 工程体系（v1-v18 历史）

PFE 已发展出完整的 18 层工程堆栈（见 `sylva_formalization/SylvaFormalization/SYLVA_PrecisionFittingEngineering_v5_44.lean`）：

| 版本 | 核心内容 | 工程涌现层级 |
|------|---------|------------|
| v1 | 工程拟合基础 | 基础涌现 |
| v2 | 精度工程（数值优化/误差控制） | 精度涌现 |
| v3 | 工业实用主义（13 行业部署） | 应用涌现 |
| v4-v5 | 端到端管道/运行时自动化 | 流程涌现 |
| v6 | 安全关键与合规 | 信任涌现 |
| v7 | 容器化与可观测性 | 部署涌现 |
| v8-v10 | 量子-经典/XAI/因果/持续学习 | 混合智能涌现 |
| v11-v13 | 自主集群/世界模型 | 系统级涌现 |
| v14-v15 | 自主研究代理/多代理 | 代理级涌现 |
| v16-v17 | 自组织研究网络/USI | 群体智能涌现 |
| v18 | LLM 集成（Pangu/DeepSeek/Claude） | 智能涌现接口 |

辅助模块：
- `EngineeringToolkit` — 跨模块工程标准
- `Templates` — 13 行业部署模板
- `TestingFramework` — 自动代理测试（替代物测试）
- `BestPractices` — 工程师手册（反模式/FAQ/调试）
- `data-storm` — 大规模数据注入与自动化

---

## 与千界花园的关系

千界花园是 PFE 的**智能涌现后端**。

- **Lean 解析**：`sylva-parser.ts` 解析 TOE-SYLVA 的 Lean 代码，提取 theorem/def/sorry
- **LLM 推理**：`research-llm.ts` 调用 Zhipu GLM-5.1 进行学术协作分析
- **学术协作**：Panel/Workshop/Pipeline/ReviewBoard 等协作组为 PFE 提供研究组织框架
- **SYLVA 同步**：`POST /api/research/sylva-sync` 将 TOE-SYLVA 的 Lean 状态同步到数据库，供 PFE 代理分析

千界花园不是前端展示工具，而是 PFE 的**智能涌现基础设施**——为 PFE 的数值计算和工程拟合提供 LLM 推理能力。

---

## 与 TOE-SYLVA 的协同

```
TOE-SYLVA（学术严格）              PFE（工程有效）
      ↓                                  ↓
  形式化定理 ←──────验证/启发──────→ 数值实验
  严格证明   ←──────近似指导──────→ 工程拟合
  千年难题   ←──────物理预言──────→ 实验设计
  0 sorry    ←──────反例发现──────→ 边界测试
```

**规则**：
- TOE-SYLVA 的定理可以作为 PFE 数值验证的目标
- PFE 的数值实验可以为 TOE-SYLVA 的定理方向提供启发
- PFE 的"不一定正确"的结果必须明确标注置信度，不污染 TOE-SYLVA 的严格性
- PFE 的 `sylva-release/` 不直接修改，只引用 TOE-SYLVA 的最新版本

---

## 工程标准

### 有效涌现评估体系

| 维度 | 评估指标 | 阈值 |
|------|---------|------|
| **置信度** | 数值结果的可重复性 | 标准差 < 10% |
| **可复现性** | 相同输入→相同输出 | 误差 < 1e-6 |
| **实用性** | 对物理/工程问题的指导价值 | 专家评分 ≥ 3/5 |
| **收敛性** | 迭代算法是否收敛 | 迭代次数 < 1000 |
| **对比性** | 与已知结果的偏差 | 与标准值偏差 < 1 个数量级 |

### 代码规范

- Python 计算脚本：使用 SageMath 9.0+ 或 Python 3.8+
- 数值结果：必须标注误差范围和置信度
- 启发式结果：必须标注"HEURISTIC"标签和失败条件
- LLM 生成：必须标注模型版本和温度参数
- 所有工程结果：必须有对应的 TOE-SYLVA 学术模块引用（反向链接）

---

## 许可证

MIT License — 工程成果开源，学术引用请指向 TOE-SYLVA。

## 联系

PFE Precision Fitting Engineering — 质空论工程原型
