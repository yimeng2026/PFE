# PFE 工程深化路线图

> 基于 PFE_MANIFESTO.md 的质空论工程原型，制定具体深化计划。

---

## Phase 1: 身份恢复（当前 — 已完成）

- [x] PFE_MANIFESTO.md — 质空论工程概念辨析
- [x] README.md — 重写为工程定位
- [x] sylva-release/README.md — 明确引用 TOE-SYLVA，不直接修改
- [x] pfe-pipelines/pfe_pipeline.py — 自动化管道入口
- [x] pfe-agents/zhikong_agent.py — 质空论代理（LLM 驱动）

---

## Phase 2: 工程扩展（下一步）

### 2.1 sagemath_verification 扩展

- [ ] 创建 `pfe-numerical/` 统一数值计算库
  - [ ] 基础数值模块（numpy/scipy 封装）
  - [ ] 复分析模块（zeta 函数数值计算、黎曼 Siegel 公式）
  - [ ] 动力系统模块（数值积分、混沌检测）
  - [ ] 概率验证模块（Monte Carlo 方法验证定理）
  - [ ] 误差分析模块（自动误差传播和置信度计算）
- [ ] 创建 `pfe-numerical/tests/` 测试套件
- [ ] 创建 `pfe-numerical/benchmarks/` 性能基准

### 2.2 alpha_derivation 工程化

- [ ] 将 `01_causal_network_simulation.py` 扩展为完整模拟引擎
- [ ] 创建不同维度（d=2,3,4,5,6）的因果网络生成器
- [ ] 实现连通性-电荷映射的数值计算
- [ ] 创建 α(d) 维度扫描脚本
- [ ] 可视化：α(d) 随维度变化曲线
- [ ] 拓扑修正：S³ vs T³ vs ℝ³ 的连通性分布对比

### 2.3 toe_framework 计算化

- [ ] 选择 5-10 个最有计算价值的框架（如量子引力、超对称、暗物质）
- [ ] 为每个框架创建参数扫描脚本
- [ ] 创建物理量计算管道（从理论参数到可测量预言）
- [ ] 建立与实验数据的对比接口

### 2.4 pfe-pipelines 管道扩展

- [ ] 创建 CI/CD 管道定义（GitHub Actions）
- [ ] 创建数据注入管道（自动从 arXiv/实验数据库获取数据）
- [ ] 创建结果验证管道（自动验证数值结果的可复现性）
- [ ] 创建报告生成管道（自动生成 Markdown/HTML 报告）
- [ ] 与千界花园 API 集成（自动提交 LLM 分析任务）

### 2.5 pfe-agents 代理扩展

- [ ] 创建多代理协作系统（Manager + Worker + Reviewer）
- [ ] 实现代理间的任务分配和结果聚合
- [ ] 创建代理记忆系统（记录历史策略和效果）
- [ ] 实现自指优化（代理评估自己的涌现质量并改进）
- [ ] 与千界花园的学术协作组接口（Panel/Workshop/Pipeline）

---

## Phase 3: 质空论涌现引擎（远期）

### 3.1 拓扑涌现器（Void → Mass）

- [ ] 从因果网络拓扑自动涌现物理参数
- [ ] 实现不同拓扑的连通性分析
- [ ] 建立拓扑-物理量映射的数据库
- [ ] 创建涌现质量评估函数

### 3.2 LLM 涌现推理引擎

- [ ] 利用 LLM 进行跨学科联想（非严格但有效的推理）
- [ ] 实现多模型集成（Pangu/DeepSeek/Claude 的涌现）
- [ ] 创建推理链的可追溯性记录
- [ ] 建立推理结果的置信度评估

### 3.3 有效涌现评估体系

- [ ] 定义完整的"有效涌现"评估标准
- [ ] 实现自动化评估管道
- [ ] 创建涌现质量的历史追踪
- [ ] 建立涌现结果的同行评审机制（代理评审）

### 3.4 千界花园集成桥接（Phase 3.5 提前完成）

- [x] `pfe_bridges/base_bridge.py` — PFEProblemBridge 抽象基类
- [x] `pfe_bridges/qianjie_bridge.py` — 千界花园 API 客户端 + 集成桥接
- [x] `pfe_bridges/agent_coordinator.py` — 多代理调度器（9 种协作类型映射）
- [x] 千界花园 API 集成（sylva-sync, modules, panels, notes）
- [x] 自动回传 PFE 验证结果到千界花园

---

## Phase 4: 与 TOE-SYLVA 的协同深化

### 4.1 双向验证管道

- [ ] TOE-SYLVA 定理 → PFE 数值验证目标（自动提取）
- [ ] PFE 数值结果 → TOE-SYLVA 定理方向启发（自动推荐）
- [ ] PFE 反例 → TOE-SYLVA 边界条件修正（自动提交）
- [ ] TOE-SYLVA 编译状态 → PFE 验证优先级调整（自动同步）

### 4.2 学术-工程桥接

- [x] 创建 `pfe_bridges/` 桥接模块目录结构
- [x] 定义 `PFEProblemBridge` 抽象基类（数值验证 + 启发式策略 + 置信度评估 + Lean↔Python 翻译）
- [x] 千界花园桥接（QianJieBridge）对接 backend API
- [x] 每个千年难题独立桥接模块（Riemann, Navier-Stokes, P vs NP, Hodge, Yang-Mills）
  - [x] `riemann_bridge.py` — 黎曼假设桥接（zeta 零点验证、Siegel 公式、粗粒化策略）
  - [x] `navier_stokes_bridge.py` — 纳维-斯托克斯桥接（Taylor-Green 涡模拟、爆破检测）
  - [x] `p_vs_np_bridge.py` — P vs NP 桥接（SAT 缩放分析、熵隙估计、电路复杂度）
  - [x] `hodge_bridge.py` — 霍奇猜想桥接（代数簇 Hodge 数计算、具体例子验证）
  - [x] `yang_mills_bridge.py` — 杨-米尔斯桥接（格点模拟、Wilson 作用量、质量隙提取）
- [x] 实现从 Lean 代码到 Python 脚本的符号翻译（`translate_lean_to_python` 方法）
- [ ] 实现全自动 Lean 符号解析（当前为手动映射，未来对接 `sylva-parser.ts`）
- [ ] 端到端自动化验证管道（PFE 调度 → 千界花园同步 → 结果聚合）

---

## 优先级矩阵

| 优先级 | 任务 | 影响 | 工作量 | 负责人 |
|--------|------|------|--------|--------|
| P0 | pfe_pipeline.py 运行并验证 | 高 | 中 | PFE |
| P0 | zhikong_agent.py LLM 调用测试 | 高 | 低 | PFE |
| P1 | sagemath_verification 扩展 | 高 | 高 | PFE |
| P1 | alpha_derivation 模拟引擎 | 高 | 中 | PFE |
| P2 | toe_framework 计算化 | 中 | 高 | PFE |
| P2 | pfe-agents 多代理协作 | 中 | 高 | PFE |
| P3 | 质空论涌现引擎 | 高 | 极高 | PFE + SYLVA |
| P3 | 学术-工程桥接 | 高 | 极高 | PFE + SYLVA |

---

## 与千界花园的集成点

| 千界花园功能 | PFE 用途 | 集成方式 |
|-------------|---------|---------|
| `sylva-parser.ts` | 解析 TOE-SYLVA Lean 代码 | Python 移植（pfe_pipeline.py） |
| `research-llm.ts` | Zhipu API 调用 | 直接调用（zhikong_agent.py） |
| `research-prompts.ts` | 学术协作提示模板 | 适配为工程协作提示 |
| `/api/research/sylva-sync` | 同步 TOE-SYLVA 状态 | 定期调用，获取最新问题 |
| `/api/research/millennium/init` | 千年难题研究生态 | 为 PFE 代理分配任务 |
| 学术协作组 | 研究组织 | PFE 代理作为"工程专家"加入 Panel |

---

**下一步立即执行**：
1. 测试 `pfe_pipeline.py` 解析 TOE-SYLVA 的 Lean 文件
2. 测试 `zhikong_agent.py` 的 LLM 调用（如果 API key 可用）
3. 提交 Phase 1 成果到 PFE 仓库
4. 继续 TOE-SYLVA 的学术 sorry 推进
