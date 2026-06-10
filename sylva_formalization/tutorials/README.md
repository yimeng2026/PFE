# Sylva 形式化教程框架

欢迎来到 Sylva 交互式形式化教程！本教程框架旨在帮助您系统地学习 Lean 4 定理证明，并深入理解 Sylva 元理论框架。

## 📚 目录结构

```
tutorials/
├── TutorialTemplate.lean           # 教程模板（创建新教程时参考）
├── 01_introduction/                # 第一章：入门
│   └── BasicTutorial.lean         # 基础教程：GF(3)、φ、七层架构
├── 02_gf3_basics/                  # 第二章：GF(3) 深入
│   └── [待创建]
├── 03_phi_calculations/            # 第三章：黄金比例计算
│   └── [待创建]
├── 04_proving_techniques/          # 第四章：证明技巧
│   └── [待创建]
├── 05_advanced_topics/             # 第五章：高级主题
│   └── [待创建]
└── README.md                       # 本文件
```

## 🚀 快速开始

### 前置要求

1. **安装 Lean 4**（如果尚未安装）：
   ```bash
   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
   source $HOME/.elan/env
   ```

2. **克隆项目并进入目录**：
   ```bash
   cd sylva_formalization
   ```

3. **获取 Mathlib 依赖**：
   ```bash
   lake update
   lake build
   ```

### 开始学习

1. **打开第一个教程**：
   ```bash
   code tutorials/01_introduction/BasicTutorial.lean
   ```
   或使用 Vim/Neovim：
   ```bash
   nvim tutorials/01_introduction/BasicTutorial.lean
   ```

2. **编译教程**（在文件所在目录）：
   ```bash
   lake build Sylva.Tutorial.Basic
   ```

3. **在 Lean 中交互式探索**：
   在 VS Code 中打开文件，将光标放在 `by` 关键字后，
   查看 Infoview 面板中的证明状态。

## 🎯 学习路径

### 路径 A：快速入门（1-2 小时）
适合：有一定函数式编程经验的学习者

1. ✅ `01_introduction/BasicTutorial.lean` - 完成所有 ⭐ 和 ⭐⭐ 练习
2. ⏳ `02_gf3_basics/` - 理解有限域理论
3. ⏳ `03_phi_calculations/` - 掌握 φ 的计算技巧

### 路径 B：系统学习（1-2 周）
适合：希望深入理解 Sylva 框架的学习者

1. ✅ `01_introduction/` - 完成所有练习（包括挑战题）
2. ✅ `02_gf3_basics/` - 深入 GF(3) 代数结构
3. ✅ `03_phi_calculations/` - 掌握黄金比例的代数性质
4. ✅ `04_proving_techniques/` - 学习高级证明策略
5. ✅ `05_advanced_topics/` - 探索综合应用

### 路径 C：证明工程师（持续）
适合：希望为 Sylva 贡献形式化证明的开发者

1. 完成所有教程
2. 阅读 `SylvaFormalization/` 中的源代码
3. 尝试填充 `sorry` 标记的未证明定理
4. 提交 Pull Request

## 📝 教程格式说明

每个教程文件遵循标准格式：

```lean
/-
================================================================================
TUTORIAL: [标题]
================================================================================
难度级别: [初级 | 中级 | 高级]
预计时间: [X] 分钟
前置教程: [列表]

学习目标:
- [目标 1]
- [目标 2]
- [目标 3]
================================================================================
-/

-- ============================================================================
-- CONCEPT: 概念讲解
-- ============================================================================
/-
🎯 核心概念: ...
💡 直观理解: ...
⚠️ 注意事项: ...
🔗 相关资源: ...
-/

-- ============================================================================
-- EXAMPLE: 完整示例
-- ============================================================================
theorem example_theorem : ... := by
  -- 详细注释的完整证明

-- ============================================================================
-- EXERCISE: 练习题
-- ============================================================================
theorem exercise_N : ... := by
  sorry  -- 在此处填入你的证明

-- ============================================================================
-- CHALLENGE: 挑战题
-- ============================================================================
theorem challenge : ... := by
  sorry  -- 挑战：完成完整证明

-- ============================================================================
-- SOLUTION: 参考答案
-- ============================================================================
theorem solution_N : ... := by
  -- 参考解答（查看前先自己尝试！）
```

### 难度标记

- ⭐ **基础**：直接应用概念，通常 1-5 行证明
- ⭐⭐ **中等**：需要组合多个策略，5-15 行证明
- ⭐⭐⭐ **困难**：需要创造性思维，15+ 行证明或需要引理
- 🏆 **挑战**：开放性问题，可能有多种解法

## 🛠️ 常用命令

### 编译
```bash
# 编译整个项目
lake build

# 编译特定模块
lake build Sylva.Tutorial.Basic

# 清理编译缓存
lake clean
```

### 交互式开发
```bash
# 启动 Lean 语言服务器（VS Code 会自动启动）
lean --server

# 检查文件是否有错误
lean tutorials/01_introduction/BasicTutorial.lean
```

### 探索项目
```bash
# 查看可用模块
lake exe cache get

# 打印依赖图
lake print-paths
```

## 📖 关键概念速查

| 概念 | 说明 | 文件位置 |
|------|------|----------|
| GF(3) | 三元素伽罗瓦域 | `BasicTutorial.lean` |
| φ (phi) | 黄金比例 (1+√5)/2 | `BasicTutorial.lean` |
| Φ_c | Sylva 临界值 = 137×φ³ | `BasicTutorial.lean` |
| D_c | 债务临界值 = φ⁴ | `BasicTutorial.lean` |
| H-CND | 七层涌现架构 | `BasicTutorial.lean` |
| M1-M7 | 元理论公理 | `BasicTutorial.lean` |

## 🔧 故障排除

### 问题：编译失败，提示找不到 Mathlib

**解决**：
```bash
lake update
lake build
```

### 问题：VS Code 中没有显示 Infoview

**解决**：
1. 确保安装了 Lean 4 扩展
2. 按 `Ctrl+Shift+P` → "Lean 4: Restart"
3. 检查右下角状态栏是否显示 "Lean: started"

### 问题：`sorry` 导致编译警告

**说明**：这是正常行为，`sorry` 是占位符，表示"此处待证明"。
完成练习后替换为实际证明代码。

### 问题：证明策略不起作用

**调试技巧**：
1. 使用 `simp?` 查看 `simp` 使用了哪些引理
2. 使用 `apply?` 让 Lean 推荐可能的策略
3. 使用 `hint` 获取证明建议

## 🤝 贡献指南

### 创建新教程

1. 复制 `TutorialTemplate.lean`：
   ```bash
   cp TutorialTemplate.lean 0N_topic/YourTutorial.lean
   ```

2. 按照模板格式填写内容

3. 更新本 README 的目录结构

4. 提交 Pull Request

### 教程质量标准

- ✅ 每个概念都有 🎯💡⚠️ 标记的说明
- ✅ 每个示例都有详细注释
- ✅ 练习题难度递增（⭐ → ⭐⭐ → ⭐⭐⭐）
- ✅ 提供参考答案（放在文件末尾的 Solutions 部分）
- ✅ 证明可编译通过（没有错误）

## 📚 延伸阅读

### Lean 4 资源
- [Lean 4 官方教程](https://leanprover.github.io/theorem_proving_in_lean4/)
- [Mathlib 文档](https://leanprover-community.github.io/mathlib4_docs/)
- [Functional Programming in Lean](https://leanprover.github.io/functional_programming_in_lean/)

### Sylva 理论资源
- `../SylvaFormalization/` - 核心形式化库
- `../README.md` - 项目总体介绍
- `../DEPENDENCIES.md` - 依赖关系说明

### 数学背景
- Galois 理论入门
- 黄金比例的代数性质
- 证明论基础

## 🐛 反馈与问题

如果您在学习过程中遇到问题：

1. 首先查看本文件的 [故障排除](#故障排除) 部分
2. 检查 Lean 社区 [Zulip](https://leanprover.zulipchat.com/) 的常见问题
3. 在项目的 Issues 页面提交问题报告

## 📜 许可证

本教程框架与 Sylva 项目使用相同的许可证。
详见项目根目录的 LICENSE 文件。

---

**Happy Proving!** 🎉

*"从 GF(3) 到无穷，从证明到真理。"*
