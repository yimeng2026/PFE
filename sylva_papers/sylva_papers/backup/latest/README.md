# Sylva Workspace 目录索引

## 📁 目录结构概览

```
/root/.openclaw/workspace/
├── archives/          # 旧版本归档
├── backups/           # 填充版本备份
├── logs/              # 编译日志和输出
├── reports/           # 标准化报告
├── sylva/             # Sylva 核心项目目录
├── sylva_formalization/  # Lean 形式化证明
└── [其他项目文件]
```

---

## 📂 详细说明

### archives/
存放旧版本文件和过时报告。

**当前内容:**
- `sylva_final_report.md` - 早期最终报告（已归档）

### backups/
存放 *_filled.lean 填充版本文件（包含完整证明的备份）。

**当前内容:**
| 文件 | 说明 | 大小 |
|------|------|------|
| Basic_filled.lean | Basic.lean 填充版本 | 3.5KB |
| BSD_filled.lean | BSD.lean 填充版本 | 18.5KB |
| Complexity_filled.lean | Complexity.lean 填充版本 | 16.2KB |
| Hodge_filled.lean | Hodge.lean 填充版本 | 19.1KB |
| NavierStokes_filled.lean | NavierStokes.lean 填充版本 | 21.6KB |
| RiemannHypothesis_filled.lean | RiemannHypothesis.lean 填充版本 | 22.1KB |

### logs/
编译日志、构建输出和验证结果。

**命名规范:** `sylva_*_log.txt`

**当前内容:**
- `pipeline.log` - 流水线执行日志
- `sylva_auto_proof_log.txt` - 自动证明日志
- `sylva_basic_filled_log.txt` - Basic.lean 填充日志
- `sylva_basic_proofs.txt` - 基础证明输出
- `sylva_final_build.log` - 最终构建日志
- `sylva_mathlib_progress.txt` - Mathlib 编译进度
- `sylva_replace_build.log` - 替换构建日志
- `sylva_rh_filled_log.txt` - RH 填充日志
- `sylva_rh_proofs.txt` - RH 证明输出
- `sylva_test_results.txt` - 测试结果
- `sylva_toolchain_check.txt` - 工具链检查
- `sylva_zeros_verification.txt` - 零点验证结果

### reports/
标准化报告，命名规范：SYLVA_* 前缀。

**当前内容 (14份报告):**

| 报告文件 | 主题 |
|----------|------|
| SYLVA_agent_config_report.md | 代理配置 |
| SYLVA_agent_core_report.md | 代理核心 |
| SYLVA_agent_docs_report.md | 代理文档 |
| SYLVA_agent_experiments_report.md | 代理实验 |
| SYLVA_agent_knowledge_report.md | 知识图谱 |
| SYLVA_agent_python_report.md | Python 代理 |
| SYLVA_agent_theory_report.md | 代理理论 |
| SYLVA_bayesian_calculator.md | 贝叶斯计算 |
| SYLVA_critical_value_physics_report.md | 临界值物理 |
| SYLVA_experimental_validation_protocol.md | 实验验证协议 |
| SYLVA_formalization_deep_dive.md | 形式化深入 |
| SYLVA_gaps_summary.md | 技术缺口汇总 |
| SYLVA_knowledge_graph_mathematical_extensions.md | 知识图数学扩展 |

### sylva/
Sylva 核心项目目录，包含：
- 阶段报告（PHASE2_REPORT.md, PHASE3_* 等）
- 技术文档（COLLATZ_MSEI_METHOD.md 等）
- 状态报告（STATUS_REPORT.md, DASHBOARD.md）
- 交付物（DELIVERABLES.md）

### sylva_formalization/
Lean 形式化证明项目：
- SylvaFormalization/*.lean - 核心形式化模块
- lakefile.toml - 项目配置
- README.md - 形式化项目说明

---

## 🚀 快速导航

| 查找内容 | 目标目录 |
|----------|----------|
| 填充版本备份 | `backups/` |
| 编译日志 | `logs/` |
| 标准化报告 | `reports/` |
| Lean 证明代码 | `sylva_formalization/` |
| 项目阶段报告 | `sylva/` |
| 旧版本文件 | `archives/` |

---

## 📝 文件命名规范

1. **报告文件:** `SYLVA_*_report.md`
2. **日志文件:** `sylva_*_log.txt`
3. **填充版本:** `*_filled.lean`
4. **临时文件:** 清理后删除

---

*最后更新: 2026-04-10*
*清理版本: v1.0*
