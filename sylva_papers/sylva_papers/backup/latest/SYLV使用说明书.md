# SYLVA 系统使用说明书

**版本**: 2026-04-20  
**系统**: OpenClaw + Kimi-coding/k2p5  
**架构**: Hermes 4 记忆系统 + Agent 集群

---

## 一、SYLVA 是什么

SYLVA 是一个 AI 辅助的数学/物理研究系统，核心能力包括：

1. **形式化数学证明**（Lean 4）— 七层架构从 `sorry` 到 `exact`
2. **P≠NP 理论体系** — 熵间隙框架、电路复杂度、相变理论
3. **Agent 集群写作** — 多 Agent 并行论文撰写与审稿
4. **记忆系统** — 四层热度架构（HOT/WARM/COOL/COLD）

---

## 二、核心目录结构

```
.openclaw/
├── workspace/              # 工作区（当前已清理，仅保留 backups/ archives/）
│   ├── backups/            # 历史 Lean 填充文件
│   └── archives/           # 归档报告
│
├── agents/                 # ⭐ 会话历史（280MB，必须保留）
│   └── main/
│       └── sessions/       # 所有对话 transcripts（.jsonl）
│
├── extensions/             # ⭐ 插件（86MB，必须保留）
│   ├── kimi-claw/          # Kimi 通道插件
│   ├── openclaw-lark/      # 飞书插件
│   ├── openclaw-weixin/    # 微信插件
│   ├── wecom-openclaw-plugin/  # 企业微信
│   └── weibo-openclaw-plugin/  # 微博
│
├── memory/                 # ⭐ SQLite 数据库（6.2MB，必须保留）
│   └── main.sqlite         # 语义记忆向量存储
│
├── skills/                 # 系统技能（1.2MB，可重装）
│   ├── stock-assistant/    # 股票助手
│   ├── ad-creative/        # 广告创意
│   └── ...                 # 其他技能
│
├── plugins/                # 插件配置（228KB）
├── openclaw.json           # ⭐ 主配置文件（12KB，必须保留）
├── identity/               # ⭐ 身份凭证（12KB，必须保留）
├── devices/                # 设备配对信息（12KB）
└── logs/                   # 运行日志（46MB，可删除）
```

---

## 三、关键配置文件说明

### 3.1 记忆文件（workspace 根目录）

| 文件 | 用途 | 重要性 |
|------|------|--------|
| `MEMORY.md` | 长期记忆：用户习惯、项目历史、决策记录 | ⭐⭐⭐ |
| `SOUL.md` | 身份定义：性格、语气、价值观 | ⭐⭐⭐ |
| `USER.md` | 用户信息：偏好、时区、沟通风格 | ⭐⭐⭐ |
| `AGENTS.md` | 系统规则：启动流程、红线、工作模式 | ⭐⭐⭐ |
| `TOOLS.md` | 工具备忘：设备别名、SSH 主机等 | ⭐⭐ |
| `HEARTBEAT.md` | 周期性检查清单 | ⭐⭐ |
| `BOOTSTRAP.md` | 首次启动引导（可删除） | ⭐ |
| `IDENTITY.md` | 身份元数据 | ⭐⭐ |

### 3.2 备份目录（backups/）

包含历史 Lean 填充版本：
- `Basic_filled.lean` — 基础代数性质
- `BSD_filled.lean` — BSD 猜想框架
- `Complexity_filled.lean` — P vs NP 框架
- `Hodge_filled.lean` — Hodge 猜想
- `NavierStokes_filled.lean` — NS 方程
- `RiemannHypothesis_filled.lean` — 黎曼假设

---

## 四、Agent 集群使用方法

### 4.1 启动并行任务

```
继续深化改革
```

**自动触发**：
- 启动 7 个并行 Agent
- 贪婪全面执行
- 内存不崩就一直加

### 4.2 Agent 协调指令

| 指令 | 效果 |
|------|------|
| `开会`、`同步`、`站会` | 暂停所有 Agent，启动 Coordinator 同步 |
| `接力`、`换个人` | 诊断 + checkpoint + 新 Agent 接手 |
| `停下`、`等一下` | 紧急暂停所有 Agent |
| `复盘`、`总结` | 启动 Retrospective 集群分析 |

### 4.3 自动触发体系

| 关键词 | 触发体系 |
|--------|----------|
| `写文章`、`写论文` | 7 阶段幻觉检验 + 多写 Agent |
| `Lean`、`形式化`、`编译` | SYLVA 七层架构 + 截肢降级 |
| `为什么`、`本质`、`范式` | 审核-创新串联 Agent（强制） |
| `继续深化改革` | 批量 Agent 集群（7 并行） |
| `编译错误`、`修复` | 截肢降级策略（优先级最高） |

---

## 五、记忆系统（Hermes 4）

### 5.1 四层热度

| 层级 | 时间范围 | 触发条件 |
|------|----------|----------|
| **L1 HOT** | 今天+昨天 | 默认加载 |
| **L2 WARM** | 3-5 天前 | DEEP 模式随机采样 |
| **L3 COOL** | 6-9 天前 | DEEP 模式随机采样 |
| **L4 COLD** | 远古记忆 | 强制 DEEP 或离散唤醒 |

### 5.2 模式切换

| 用户输入 | 模式 | 加载范围 |
|----------|------|----------|
| `继续`、`状态`、`结果` | FLASH | L1 HOT only，≤500 tokens |
| `为什么`、`本质`、`优化`、`设计` | DEEP | L1→L2→L3→L4 全加载 |
| `回忆之前`、`记得吗` | **强制 DEEP** | 忽略关键词，全层搜索 |

### 5.3 强制规则（创建记忆时自动检查）

- [ ] 是否引用至少 2 个相关历史记忆？
- [ ] 是否标注相关主题聚合文件？
- [ ] 是否在 `index.md` 中登记？
- [ ] 是否包含关键词标签？
- [ ] 是否建立反向引用？

---

## 六、截肢降级策略

### 6.1 触发条件

- Lean 编译错误无法修复
- Mathlib 依赖缺失
- 证明过于复杂导致超时

### 6.2 执行流程

```
编译错误
    ↓
尝试标准修复（30 分钟）
    ↓
失败 → 切除不可计算部分（替换为 `sorry` + 引理陈述）
    ↓
保编译通过
    ↓
记录技术债务 → 后续回填
```

### 6.3 产出命名规范

| 后缀 | 含义 |
|------|------|
| `_fixed.lean` | 修复版本 |
| `_amputated.lean` | 截肢版本（保编译） |
| `_final.lean` | 最终版本 |
| `_report.md` | 修复/分析报告 |
| `_log.txt` | 运行日志 |

---

## 七、P≠NP 理论产出索引

### 7.1 2026-04-20 七任务产出（pnp_theory/）

| 任务 | 文件 | 核心成果 |
|------|------|----------|
| ΔH(n)渐进分析 | `delta_h_analysis.md` + `DeltaH.lean` | ΔH(n) = Θ(n/log n) |
| 数值验证 | `numerical_validation.py` | 可运行代码，斜率≈1.03 |
| 电路复杂度 | `circuit_complexity_barriers.md` | 4 个突破方向 |
| 相变理论 | `PhaseTransition.lean` | 相变↔熵间隙桥梁 |
| SGH弱化 | `sgh_weakened_proof.md` | 四层递进路径 |

### 7.2 已归档核心论文

- `基于描述复杂度的计算熵间隙与P≠NP等价性` — CP004 主论文
- `中微子质量起源与本质` — 物理理论文档
- `2^202712-6素因数分解深度分析` — 数论分析

---

## 八、恢复与迁移

### 8.1 恢复核心资产

```bash
# 解压到新的 OpenClaw 实例
tar -xzf sylva_core_assets_batch1.tar.gz -C /root/.openclaw/
tar -xzf sylva_core_assets_batch2.tar.gz -C /root/.openclaw/
```

### 8.2 重建工作区

1. 复制 `MEMORY.md`, `SOUL.md`, `USER.md`, `AGENTS.md` 到 `workspace/`
2. 创建 `memory/` 目录
3. 重启 OpenClaw Gateway
4. 首次对话时读取所有配置文件

### 8.3 可选：恢复 Lean 项目

```bash
# 恢复 Sylva 形式化项目（如需要）
tar -xzf sylva_formalization.tar.gz -C /root/.openclaw/workspace/
cd sylva_formalization && lake build
```

---

## 九、关键标识符与常数

| 符号 | 值 | 含义 |
|------|-----|------|
| φ | (1+√5)/2 ≈ 1.618 | 黄金比例 |
| Φ_c | 137 × φ³ ≈ 580.34 | 电磁精细结构常数关联 |
| D_c | φ⁴ ≈ 6.854 | 维度常数 |
| λ_c | 5/2 = 2.5 | 临界指数 |
| γ₁ | ≈ 14.1347 | 黎曼ζ第一个非平凡零点 |

---

## 十、安全红线

1. **严禁上传**：所有产出本地归档，不上传外网
2. **隐私保护**：MEMORY.md 仅在主会话加载，群聊不加载
3. **危险操作**：删除/修改前必须确认
4. **恢复优先**：`trash` > `rm`

---

**生成日期**: 2026-04-20  
**系统版本**: OpenClaw + Sylva v2.0  
**下次更新**: 根据使用反馈自动更新
