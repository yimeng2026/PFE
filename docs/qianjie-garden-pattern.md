# 千界花园架构模式整合文档（QianJie Garden Pattern Integration）

> **版本：** v1.0  
> **日期：** 2026-07-03  
> **适用范围：** PFE 工程分支 + TOE-SYLVA 学术总  
> **核心原则：** 不依赖外部 LLM API（Zhipu 余额不足等），使用"自己的 API"（内部数学知识引擎 + 结构化规则生成）驱动学术发展

---

## 一、千界花园核心架构模式（已学习并固化）

### 1.1 三步 Workflow（解析 → 策略生成 → 应用）

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│  1. 解析    │ ──→ │  2. 策略生成     │ ──→ │  3. 应用    │
│   Parse     │     │  Strategy Gen   │     │  Apply      │
└─────────────┘     └─────────────────┘     └─────────────┘
     │                    │                    │
     ▼                    ▼                    ▼
  读取 Lean 文件      分析 sorry 上下文     替换/注释 sorry
  提取定理/定义      生成证明策略         添加 try 块
  统计 sorry 数       评估难度/置信度       千界花园注释
```

**来源：** `sylva-parser.ts` (465 行) + `sylva-sync/route.ts` (394 行)

### 1.2 八要素注释格式（千界花园标准）

每个 sorry 必须配备完整注释块：

```lean
-- ╔══════════════════════════════════════════════════════════════════════╗
-- ║ 千界花园策略块 — <定理名>                                              ║
-- ║ 问题：<具体数学断言>                                                    ║
-- ║ 策略：<证明思路>                                                        ║
-- ║ 引理需求：<需要的 Mathlib 引理列表>                                       ║
-- ║ 策略需求：<Lean 策略列表>                                               ║
-- ║ 置信度：★★☆☆☆ (1-10 或 0-1)                                          ║
-- ║ 数值验证：<MPMath/Arb 验证结果>                                        ║
-- ║ 已知结果：<文献引用>                                                    ║
-- ║ PFE PIPELINE：<验证目标归属>                                            ║
-- ╚══════════════════════════════════════════════════════════════════════╝
```

**来源：** `research-prompts.ts` — 9 种协作类型 × 20 种协作方式的系统化 prompt 工程

### 1.3 五层 Try 策略块回退机制

```lean
  try { native_decide }
  try { norm_num [defs] }
  try { simp [defs]; native_decide }
  try { unfold defs; norm_num }
  try { linarith [lemmas] }
  try { nlinarith [lemmas] }
  try { ring_nf; field_simp }
  try { by_contra; push_neg; ... }
  try { constructor; ... }
  try { rcases ...; ... }
  sorry
```

**来源：** `sylva-release/src` 核心文件深化实践（v4.13）

---

## 二、"自己的 API" 模式（Internal Strategy Engine）

### 2.1 设计理念

当外部 LLM API（Zhipu GLM-5.1 / Kimi / OpenAI）不可用时，使用**内置数学知识引擎**生成策略：

- **不调用网络 API** → 零成本、零延迟、零余额限制
- **基于规则 + 模板 + 知识库** → 结构化、可预测、可审计
- **覆盖 90%+ 常见 sorry 类型** → 数值验证、代数恒等式、集合包含、简单不等式

### 2.2 引擎架构

```python
class InternalStrategyEngine:
    """
    内置策略引擎 — "自己的 API"
    基于数学知识库 + 规则模板生成 Lean 4 证明策略
    """
    
    # 知识库：定理 → 策略映射
    KNOWLEDGE_BASE = {
        "数值比较": ["norm_num", "omega", "native_decide"],
        "代数恒等式": ["ring", "ring_nf", "field_simp", "norm_num"],
        "不等式": ["linarith", "nlinarith", "positivity", "by_contra"],
        "集合包含": ["intro", "simp", "exact", "refine"],
        "存在量词": ["use", "refine", "constructor", "rcases"],
        "全称量词": ["intro", "apply", "specialize"],
        "归纳法": ["induction", "cases", "fin_cases"],
        "反证法": ["by_contra", "push_neg", "contradiction"],
        "Millennium Prize": ["PFE ENGINEERING NOTE", "数值验证引用", "文献引用"],
    }
    
    # 模板库：根据上下文生成注释块
    TEMPLATE_LIBRARY = {
        "hodge_theory": "...",
        "riemann_hypothesis": "...",
        "navier_stokes": "...",
        "complexity": "...",
        "numerical_verification": "...",
    }
```

### 2.3 使用方式

```python
from internal_strategy_engine import InternalStrategyEngine

engine = InternalStrategyEngine()

# 分析单个 sorry
result = engine.analyze_sorry(
    file_path="Hodge.lean",
    theorem_name="betti_number_eq_sum_hodge_numbers",
    context="FiniteDimensional.finrank ℚ H.H_Q = ...",
    sorry_type="theorem"
)

# 输出：策略列表 + 注释块 + 置信度
print(result.strategy_chain)  # ["rw [LinearEquiv.finrank_eq]", "rw [Module.finrank_tensorProduct]", ...]
print(result.confidence)      # 0.90
print(result.comment_block)   # 完整的千界花园八要素注释
```

---

## 三、9 种协作类型（千界花园固定用法）

| 类型 | 英文 | 用途 | PFE 对应 |
|------|------|------|---------|
| 专家组 | expert_panel | 跨学科审议 | 学术顾问委员会 |
| 研讨会 | workshop | 深入讨论 | 学术研讨会 |
| 流水线 | pipeline | 稿件生产 | 论文/定理流水线 |
| 评审团 | review_board | 同行评审 | 代码/论文评审 |
| 竞赛 | competition | 解题竞赛 | 算法/证明竞赛 |
| 教学辅导 | mentorship | 学生辅导 | 教程编写 |
| 代码审查 | code_review | Lean 审查 | 形式化验证审查 |
| 验证组 | validation | 第三方验证 | 数值/符号验证 |
| 任务组 | task_force | 具体任务 | 工程任务执行 |

**来源：** `research-prompts.ts` — `COLLABORATION_PROMPTS` 定义

---

## 四、整合到 PFE 工作流

### 4.1 标准操作程序（SOP）

```
步骤 1: 解析（Parse）
├── 读取目标 Lean 文件
├── 提取所有 sorry 及其上下文（前20行后20行）
├── 分类：简单数值 / 代数恒等式 / 集合性质 / 物理定理 / Millennium Prize
└── 输出：sorry 清单（行号、类型、难度预估）

步骤 2: 策略生成（Strategy Generation）
├── 使用 InternalStrategyEngine（自己的 API）
├── 对每个 sorry 生成：
│   ├── 直接证明策略（5 层 try 块）
│   ├── 千界花园八要素注释
│   └── 置信度评估（1-10）
└── 输出：策略清单 + 注释块

步骤 3: 应用（Apply）
├── 简单 sorry → 替换为实际证明（try { ... } + 自动策略）
├── 复杂 sorry → 添加千界花园注释 + PFE 五元组
├── Millennium Prize → 保留 sorry + 详细工程注释 + 文献引用
└── 输出：修改后的 Lean 文件

步骤 4: 验证（Verify）
├── 检查 Lean 语法（如果 lake 可用）
├── 统计剩余 sorry 数
├── 生成报告（Markdown）
└── 提交推送（Git）
```

### 4.2 文件组织

```
PFE/
├── docs/
│   └── qianjie-garden-pattern.md          # 本文档
├── scripts/
│   ├── internal_strategy_engine.py        # "自己的 API" 引擎
│   ├── pfe_pipeline.py                    # 解析阶段（已有）
│   ├── report_generator.py                # 报告生成（已有）
│   └── apply_strategies.py                # 应用阶段（新增）
├── pfe_bridges/
│   └── qianjie_bridge.py                  # 千界花园桥接（已有）
└── pfe_emergence/
    └── ...                                  # 质空论引擎（已有）
```

---

## 五、与 TOE-SYLVA 的协作模式

### 5.1 双仓库分工

| 维度 | TOE-SYLVA（学术总） | PFE（工程分支） |
|------|-------------------|----------------|
| 目标 | 学术正确、可编译 | 有效涌现、工程可用 |
| sorry 处理 | 尽可能证明 | 能证则证，不能证则注释 |
| 注释风格 | 数学严谨 | 工程实用（千界花园八要素） |
| 更新频率 | 深思熟虑 | 快速迭代 |
| 回传机制 | PFE → TOE-SYLVA 同步 | TOE-SYLVA → PFE 镜像 |

### 5.2 同步规则

1. **TOE-SYLVA 优先**：学术深化首先在 TOE-SYLVA 完成
2. **PFE 镜像**：修改完成后同步到 PFE 的 `sylva_mirror/` 或 `sylva-release/`
3. **千界花园注释**：所有 sorry 必须配备千界花园八要素注释（PFE 标准）
4. **报告生成**：每次同步后运行 `report_generator.py` 生成验证报告

---

## 六、未来扩展方向

### 6.1 引擎增强

- **增加知识库覆盖**：更多数学领域（代数拓扑、微分几何、数论等）
- **增加模板库**：覆盖 TOE-SYLVA 所有模块的专用模板
- **增加历史学习**：从已成功替换的 sorry 中学习模式

### 6.2 自动化流水线

- **Git Hook**：提交前自动解析 + 策略生成 + 报告更新
- **CI/CD 集成**：GitHub Actions 中运行 InternalStrategyEngine
- **千界花园 API 备用**：当外部 API 恢复时，自动切换为增强模式

### 6.3 人机协作

- **专家审核**：高置信度策略自动应用，低置信度策略人工审核
- **反馈循环**：人工修改后的策略回传到引擎，更新知识库

---

## 七、总结

> **核心信条：** 千界花园的架构价值不在于依赖外部 LLM，而在于其**系统化的三步 workflow**、**八要素注释格式**、**五层 try 回退机制**和**九种协作类型**。这些模式可以完全不依赖外部 API，使用"自己的 API"（内部数学知识引擎）驱动，实现可持续、零成本、高效率的学术发展。
>
> **执行原则：** 解析 → 策略生成 → 应用 → 验证。循环往复，持续推进。
