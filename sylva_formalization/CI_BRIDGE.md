# Mega ↔ Sylva Formalization CI Bridge

## 概述

本桥接方案将 Sylva 七层架构的 Lean 4 形式化证明项目 (`sylva_formalization/`) 接入 Mega 的 CI 流程，实现自动编译验证、状态面板反馈和 Agent 修复触发。

---

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         Mega CI Pipeline                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐ │
│  │  test-      │  │  test-      │  │ lean-       │  │ docker │ │
│  │  gateway    │  │  frontend   │  │ formaliz-   │  │ build  │ │
│  │  (Node.js)  │  │  (Node.js)  │  │ ation       │  │        │ │
│  └─────────────┘  └─────────────┘  └──────┬──────┘  └────────┘ │
│                                           │                      │
│                              ┌────────────▼────────────┐         │
│                              │   scripts/lean-ci.sh   │         │
│                              │  (Toolchain detection   │         │
│                              │   + lake build + skip)  │         │
│                              └────────────┬────────────┘         │
│                                           │                      │
│                    ┌──────────────────────┼──────────────────┐ │
│                    │                      │                  │ │
│           ┌────────▼────────┐    ┌───────▼────────┐        │ │
│           │  lake build     │    │ LeanBuildReporter│        │ │
│           │  (sylva_formal) │    │   (Python)       │        │ │
│           └────────┬────────┘    └───────┬────────┘        │ │
│                    │                      │                  │ │
│           ┌────────▼────────┐    ┌───────▼────────┐        │ │
│           │ .lake/build/lib │    │ JSON Report    │        │ │
│           │    .olean      │    │ + MD Summary   │        │ │
│           └─────────────────┘    └───────┬────────┘        │ │
│                                          │                  │ │
│                    ┌─────────────────────┘                  │ │
│                    │                                         │ │
│           ┌────────▼────────┐                               │ │
│           │ Mega Status     │                               │ │
│           │ Panel (turbo/   │                               │ │
│           │   GH Actions)   │                               │ │
│           └─────────────────┘                               │ │
│                                                             │ │
│  Agent Repair Trigger (on failure)                          │ │
│  ├── .agent_repair_trigger_<timestamp>  (marker file)        │ │
│  └── OpenClaw Agent 自动修复流程                              │ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 文件清单

| 文件 | 作用 | 修改/新增 |
|------|------|-----------|
| `scripts/lean-ci.sh` | Lean CI 主脚本：工具链检测、lake build、报告生成 | **新增** |
| `scripts/ci.sh` | Mega 统一 CI 编排脚本（可选入口） | **新增** |
| `scripts/LeanBuildReporter.py` | 结构化报告生成器（JSON + Markdown） | **新增** |
| `sylva_formalization/lakefile_ci_adapter.sh` | lakefile 内部 CI 适配脚本 | **新增** |
| `.github/workflows/ci.yml` | GitHub Actions 工作流，新增 `lean-formalization` job | **修改** |
| `turbo.json` | 新增 `lean-ci` task 定义 | **修改** |
| `package.json` | 新增 `lean-ci` npm scripts | **修改** |
| `sylva_formalization/.lake/build/reports/` | 报告输出目录（运行时生成） | 运行时 |

---

## 使用方式

### 本地运行

```bash
# 直接运行 Lean CI（自动检测工具链，缺失则跳过）
npm run lean-ci

# 或使用 turbo
npx turbo run lean-ci

# 生成基线（用于后续对比）
npm run lean-ci:baseline

# 对比基线生成报告
npm run lean-ci:report
```

### GitHub Actions

已在 `.github/workflows/ci.yml` 中新增 `lean-formalization` job：
- 自动检测 `lake` 是否安装
- 未安装时尝试通过 elan release 二进制安装
- 运行 `./scripts/lean-ci.sh --skip-if-missing --verbose`
- 上传 JSON 报告为 Artifact
- PR 失败时自动评论 Lean 状态

### 统一 CI 入口

```bash
# 运行全部 CI 阶段
./scripts/ci.sh all

# 仅运行 Lean
./scripts/ci.sh lean

# 仅运行 Node.js
./scripts/ci.sh node
```

---

## 报告格式

### JSON 报告 (`lean_ci_report_<timestamp>.json`)

```json
{
  "timestamp": "2026-05-18T22:35:00+08:00",
  "status": "success",
  "reason": null,
  "toolchain": "leanprover/lean4:v4.29.0",
  "lean_version": "Lean (version 4.29.0, commit xxxxx)",
  "lake_version": "Lake version 5.0.0-src+98dc76e",
  "elapsed_seconds": 45.2,
  "build_success": true,
  "build_exit_code": 0,
  "sorry_count": 12,
  "sorry_delta": +3,
  "error_count": 0,
  "error_delta": 0,
  "modules": [
    { "name": "NavierStokes", "line_count": 340, "sorry_count": 2, "has_been_amputated": true },
    { "name": "CookLevin",    "line_count": 280, "sorry_count": 1, "has_been_amputated": false }
  ],
  "agent_repair_triggered": false
}
```

### Markdown 摘要 (`lean_report_latest.md`)

生成人类可读的状态面板摘要，包含：
- 编译状态（✅/❌）
- `sorry` 数量及基线对比（🔴/🟢）
- 各模块摘要表（含截肢标记 🔪）
- 错误列表
- Agent 修复触发状态

---

## 工具链检测逻辑

`scripts/lean-ci.sh` 按以下优先级检测 Lean 工具链：

1. 环境变量：`LAKE_CMD`、`LEAN_CMD`、`ELAN_CMD`
2. `which lake` / `which lean`
3. 常见安装路径：
   - `~/.elan/bin/`
   - `/usr/local/bin/`
   - `/usr/bin/`
   - `~/.local/bin/`
4. Windows 兼容：检查 `lake.exe`

若全部未找到且 `--skip-if-missing` 启用：
- 生成 "skipped" 状态报告
- CI **不阻塞**，继续后续阶段
- 报告记录 `reason: "lean_toolchain_not_found"`

---

## Agent 修复触发

当编译失败时：
1. 在 `sylva_formalization/.lake/build/reports/` 下创建 `.agent_repair_trigger_<timestamp>` 标记文件
2. 标记文件包含：报告路径、日志路径、时间戳、错误数量
3. Mega 状态面板或 OpenClaw Agent 可轮询此目录触发自动修复流程

---

## Lean 版本特殊性

| 特性 | 处理方式 |
|------|----------|
| **elan 管理** | 检测 `~/.elan/bin/`，支持多版本切换 |
| **lake-manifest.json** | 构建前检查，缺失时仅警告 |
| **mathlib 依赖** | 通过 `--offline` 模式支持无网络 CI 环境 |
| **工具链不匹配** | 对比 `lean-toolchain` 与 `lean --version`，发出 warn |
| **Windows / WSL** | 支持 `lake.exe` 跨平台调用 |

---

## 安全与保密

- 所有报告和日志**本地归档**，不上传到任何外部服务
- GitHub Actions Artifact 仅在 CI 运行时临时存在
- 标记文件中的路径为相对路径，不含敏感信息
- 符合 Mega "本地归档，严禁上传" 红线

---

## 后续扩展

1. **增量编译**：利用 `.lake/build/lib` 缓存 `.olean`，实现增量 CI
2. **sorry 趋势图**：长期追踪 `sorry_count` 变化，生成趋势图表
3. **模块级 Gate**：对关键模块（如 `NavierStokes`、`RiemannHypothesis`）设置独立编译阈值
4. **自动截肢降级**：编译失败时自动回退到 `_amputated.lean` 版本再试
