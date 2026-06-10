# Lean 4 + Mathlib4 工具链指南

> **收集时间**: 2026-06-03
> **适用范围**: Lean 4 v4.9+ / Mathlib4 最新稳定版
> **作者**: SYLVA 自动收集

---

## 目录

1. [Lean 4 版本演进与关键更新](#1-lean-4-版本演进与关键更新)
2. [Mathlib4 模块状态概览](#2-mathlib4-模块状态概览)
3. [Lean 4 Windows 平台编译问题与解决方案](#3-lean-4-windows-平台编译问题与解决方案)
4. [Lake Build 最佳实践与缓存策略](#4-lake-build-最佳实践与缓存策略)
5. [Grind 战术系统深度解析](#5-grind-战术系统深度解析)
6. [已知问题速查表](#6-已知问题速查表)
7. [参考链接汇总](#7-参考链接汇总)

---

## 1. Lean 4 版本演进与关键更新

### 版本时间线

| 版本 | 发布日期 | 关键特性 |
|------|----------|----------|
| v4.20.0 | 2025-06-02 | Lake改进，`extract_lets`/`lift_lets` 战术，grind CommRing基础 |
| v4.21.0 | 2025-08-?? | grind 模型组合(MBTC)，Coinductive predicates |
| v4.22.0 | 2025-09-?? | 改进的功能归纳原理，coinductive/least_fixpoint |
| v4.23.0 | 2025-10-?? | String类型重设计，异步原语扩展 |
| v4.24.0 | 2025-11-?? | grind交互模式，远程缓存支持 |
| v4.25.0 | 2025-11-14 | **远程缓存正式支持**，grind injective函数支持，ordered ring结构 |
| v4.26.0 | 2025-12-?? | 模块系统实验性改进 |
| v4.27.0 | 2026-01-?? | bv_decide优化，cutsat改进 |
| v4.28.0 | 2026-02-17 | **模块系统修复**，bv_decide性能提升，grind标注扩展 |

### v4.25.0 重大更新（强烈推荐关注）

#### 1. 远程缓存（Remote Caching）

PR #10188 为 Lake 引入了对远程构件缓存的支持（例如 Reservoir）。

**新增 CLI 命令**:
```bash
lake cache get          # 下载远程缓存
lake cache put          # 上传本地缓存
lake cache clean        # 清理缓存
lake cache stat         # 查看缓存统计
```

**配置 lakefile.toml**:
```toml
[cache]
remote = "https://reservoir.lean-lang.org/api/v1/cache"
```

#### 2. Grind 战术重大增强

- **Injective函数支持**: `[grind inj]` 属性标记单射定理
- **Ordered Ring结构**: 支持预序和有序环结构
- **交互模式**: `grind?` 生成可复制证明脚本
  - 支持 `intro`, `intros`, `assertNext`, `assertAll`, `splitNext`
  - 支持 `lia`, `linarith`, `ac`, `ring`, `cases?` 等动作
- **E-matching改进**: 新的模式推断启发式（默认启用）
  - 回退旧行为: `set_option backward.grind.inferPattern true`
- **代码动作**: `set_option grind.param.codeAction true` 启用grind参数代码动作

#### 3. 语言特性

- **自动化规范定理生成**: 类型类方法的自动规范定理
- **Coinductive谓词**: 基于格论结构的最小/最大不动点
- **mvcgen不变式建议**: `mvcgen?` 提示辅助

#### 4. 标准库

- `String` 类型重新设计
- 异步 IO 多路复用框架
- `RArray` 宇宙多态性

### v4.28.0 最新更新 (2026-02-17)

- **模块系统修复**: 多项模块系统问题修复
- **bv_decide性能**: SAT求解器可配置 `solverMode`
- **grind标注扩展**: 更多库标注了grind支持
- **Sym框架**: 符号模拟框架的新模式匹配与统一过程

### 调试选项

```lean
set_option grind.debug true           # 启用grind调试输出
set_option grind.param.codeAction true  # 启用grind代码动作
set_option debug.terminalTacticsAsSorry true  # 终端战术替换为sorry（调试启动问题）
set_option backward.grind.inferPattern true   # 使用旧版模式推断
set_option backward.privateInPublic true      # 允许跨模块访问私有声明（迁移辅助）
```

---

## 2. Mathlib4 模块状态概览

### 2.1 Number Theory（数论）

**状态**: 🟢 活跃发展，核心基础完善

**已形式化内容**:
- 基本数论: 素数、素数定理(PNT)、算术函数、模运算
- 代数数论: Dedekind域、分式理想、类数
- 解析数论: Zeta函数、Dirichlet特征、素数分布
- 丢番图方程: 一些经典方程的解

**活跃项目**:
- **Prime Number Theorem And**: Alex Kontorovich 和 Terry Tao 的形式化素数定理项目
  - 仓库: https://github.com/AlexKontorovich/PrimeNumberTheoremAnd
- **Goldbach Conjecture**: 相关弱化形式的形式化探索
  - 仓库: https://github.com/leanprover-community/mathlib4 (相关讨论)
- **Riemann Hypothesis相关**: 形式化黎曼假设的工作在进展中
  - 参考: B. Gomes 和 A. Kontorovich 的 Lean Riemann Hypothesis 项目

**缺失/待完善**:
- 完整的Goldbach猜想（强形式）尚未形式化
- 完整的Riemann Hypothesis证明框架
- 高级解析数论工具（如圆法等）

### 2.2 Analysis（分析）

**状态**: 🟢 高度成熟，持续扩展

**已形式化内容**:
- **测度论**: σ-代数、测度空间、Lebesgue积分、Radon-Nikodym定理
- **微积分**: 单变量/多变量微积分、基本定理
- **复分析**: 全纯函数、Cauchy积分定理、留数定理、Riemann映射定理（形式化中）
- **泛函分析**: Banach空间、Hilbert空间、有界算子、谱定理（2026年完成）
  - 参考: https://github.com/leanprover-community/mathlib4/pull/??（谱定理形式化）
- **概率论**: 概率空间、随机变量、期望、方差、大数定律
- **傅里叶分析**: Fourier变换基础

**活跃讨论** (Zulip 2025年3月):
- Riemann映射定理的形式化
- 符号积分/微分形式
- 拓扑向量空间扩展

**最近进展**:
- 谱定理的完整形式化（有界和无界线性算子）
- 基本定理变体的形式化
- 复上半平面的Moebius作用

### 2.3 Algebra（代数）

**状态**: 🟢 最成熟模块之一

**已形式化内容**:
- 群论: 从基本定义到有限单群分类的一部分
- 环论: 交换代数、Dedekind域、局部化
- 域论: Galois理论、代数闭域
- 模论: 自由模、投射模、内射模
- 同调代数: 链复形、同调群、Ext/Tor
- 表示论: 特征标理论基础
- 范畴论: 丰富的范畴论基础设施

**活跃项目**:
- 代数几何基础（Schemes等）
- 更高级的交换代数工具
- 同伦代数

### 2.4 Topology（拓扑）

**状态**: 🟢 核心部分完善，高级主题在扩展

**已形式化内容**:
- 点集拓扑: 连续映射、紧致性、连通性、分离公理
- 代数拓扑: 基本群、覆叠空间
- 微分拓扑: 流形（带边界/角）、切丛
- CW复形: 形式化已完成
  - 参考论文: Hannah Scholz 的硕士论文 "Formalisation of CW-complexes"
- 同伦论: 基础定义，Whitehead定理待形式化

**活跃讨论** (Zulip 2025年3月):
- `Topology/Homeomorph` 的拆分重构
- `Prop` 上的拓扑
- 正则语言的拓扑特征
- 拓扑群

**最近进展**:
- CW-复商的商空间形式化
- 同伦扩展性质
- 紧致流形与有限CW复形的关系

### 2.5 Computability（可计算性）

**状态**: 🟡 基础存在，高级主题待扩展

**已形式化内容** (来自 mathlib-overview):
- 可计算函数: 一般递归函数、图灵机
- 原始递归函数、Ackermann函数
- 图灵机、停机问题、Rice定理
- 图灵度
- 多项式时间计算
- 形式语言:
  - DFA, NFA, ε-NFA, 正则表达式
  - 上下文无关语言、上下文无关文法
  - Arden引理

**缺失/待完善** (2025年波恩大学学生项目笔记):
- **NP类尚未定义**（关键缺失！）
- Cook定理（SAT是NP完全的）尚未形式化
- 复杂度类的完整层次结构
- 可计算性理论的高级结果

**相关项目**:
- 学生项目: https://git.abstractnonsen.se/max/mathlib4
- 目标: 形式化Cook定理，需要先定义NP类
- 上下文无关文法已有 `IsContextFree` 谓词

---

## 3. Lean 4 Windows 平台编译问题与解决方案

### 3.1 环境要求

- **必需**: Windows 10/11 64位
- **必需**: PowerShell（推荐作为默认终端）
- **必需**: Git（用于依赖下载）
- **必需**: Visual Studio Code + Lean 4 扩展

### 3.2 已知问题与修复

#### 问题 1: PATH 配置错误

**症状**:
```
'lake' 不是内部或外部命令
'elan' 不是内部或外部命令
```

**解决**:
```powershell
# 检查 elan 是否安装
~/.elan/bin/elan --version

# 手动添加 PATH（PowerShell）
$env:Path += ";$env:USERPROFILE\.elan\bin"

# 永久添加（系统环境变量）
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:USERPROFILE\.elan\bin", "User")
```

#### 问题 2: Unicode 路径问题

**症状**: 项目路径包含中文/Unicode字符时编译失败

**解决**:
- 将项目移动到纯ASCII路径，例如 `C:\lean\myproject`
- 避免用户名包含非ASCII字符

#### 问题 3: VS Code 扩展 "Waiting for Lean Server"

**症状**: Lean服务器无法启动

**解决步骤**:
1. 确认使用 **"Open Folder"** 打开包含 `lakefile.toml/lean` 的目录
2. 不要单独打开单个 `.lean` 文件
3. 检查 `lean-toolchain` 文件是否存在
4. 重启 VS Code

#### 问题 4: GitHub 下载超时（中国大陆地区）

**症状**:
```
Failed to connect to github.com port 443: Timeout
```

**解决选项**:

**选项 A: 配置代理**
```powershell
$env:https_proxy = "socks5://your-proxy:port"
elan toolchain install nightly
```

**选项 B: 手动下载 + 本地安装**
```powershell
# 从其他渠道下载 elan/lean 二进制文件
# 手动放置在 ~/.elan/toolchains/ 目录下
# 创建 toolchain 链接
```

**选项 C: 使用 elan 环境变量**
```powershell
$env:ELAN_USE_REQWEST = "false"  # 强制使用 curl 后端
```

#### 问题 5: lake update 失败

**症状**: 依赖下载失败或版本不匹配

**解决**:
```bash
# 清理并重新获取依赖
lake clean
rm -rf .lake/packages
lake update

# 如果仍失败，检查 lean-toolchain 文件
# 确保与 mathlib 的 toolchain 一致
cat lean-toolchain
# 应显示类似:leanprover/lean4:v4.25.0
```

#### 问题 6: 构建时内存不足

**症状**: 编译大型文件时崩溃

**解决**:
```toml
# lakefile.toml 中添加
[leanOptions]
maxHeartbeats = 1000000  # 增加心跳数
# 或环境变量
$env:LEAN_CC = "gcc"  # 确保使用正确编译器
```

### 3.3 Windows 安装最佳实践

```powershell
# 1. 安装 elan（使用官方脚本）
# 在 PowerShell 中执行:
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/leanprover/elan/master/elan-init.ps1" -OutFile "elan-init.ps1"
# 或使用 MSYS2/MinGW 环境

# 2. 验证安装
elan --version
lake --version
lean --version

# 3. 创建新项目
lake new myproject

# 4. 如果是 mathlib 项目
cd myproject
# 编辑 lakefile.toml 添加 mathlib 依赖
lake update
lake exe cache get  # 下载 mathlib 缓存（推荐！）

# 5. 构建
lake build
```

### 3.4 推荐配置

```toml
# lakefile.toml
name = "MyProject"
version = "0.1.0"
defaultTargets = ["MyProject"]

[leanOptions]
pp.unicode.fun = true
autoImplicit = false

# Windows 特定: 设置最大内存
maxHeartbeats = 200000

[[require]]
name = "mathlib"
scope = "leanprover-community"
rev = "v4.25.0"  # 使用稳定版本

[[lean_lib]]
name = "MyProject"
```

---

## 4. Lake Build 最佳实践与缓存策略

### 4.1 基本命令速查

```bash
# 项目初始化
lake new <project-name>          # 创建新项目
lake init <project-name>         # 在现有目录初始化

# 依赖管理
lake update                      # 更新所有依赖
lake update mathlib              # 更新指定依赖
lake build                       # 构建项目
lake clean                       # 清理构建产物

# 执行
lake exe <target>                # 运行可执行文件

# 缓存 (v4.25.0+)
lake cache get                   # 下载远程缓存
lake cache put                   # 上传本地缓存
lake cache clean                 # 清理缓存
lake cache stat                  # 查看缓存状态

# 其他
lake setup-file <file>           # 设置文件构建
lake serve                       # 启动语言服务器
```

### 4.2 缓存策略详解

#### 本地缓存

Lake 自动管理本地缓存，存储在 `.lake/build/` 目录下。

#### 远程缓存（推荐用于 mathlib 项目）

**mathlib 缓存下载** (v4.25.0之前):
```bash
# 旧方式（仍然有效）
lake exe cache get
```

**新方式** (v4.25.0+):
```bash
# 使用内置 cache 命令
lake cache get

# 指定缓存源
lake cache get --from https://reservoir.lean-lang.org
```

#### CI/CD 缓存配置 (GitHub Actions)

```yaml
# .github/workflows/build.yml
name: Build

on: [push, pull_request]

jobs:
  build:
    runs-on: windows-latest  # 或 ubuntu-latest, macos-latest
    steps:
      - uses: actions/checkout@v4
      
      # 缓存 .lake 目录
      - uses: actions/cache@v4
        with:
          path: .lake
          key: ${{ runner.os }}-lake-${{ hashFiles('lake-manifest.json') }}
          restore-keys: |
            ${{ runner.os }}-lake-
      
      # 安装 elan
      - name: Install elan
        run: |
          curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh
          echo "$HOME/.elan/bin" >> $GITHUB_PATH
        shell: bash
      
      # 下载缓存
      - name: Download cache
        run: lake cache get || lake exe cache get
      
      # 构建
      - name: Build
        run: lake build
```

### 4.3 加速构建的技巧

1. **使用预编译缓存**:
   ```bash
   lake exe cache get  # 必须在新克隆后执行
   ```

2. **并行构建**:
   ```bash
   lake build -j$(nproc)  # Linux/macOS
   lake build -j %NUMBER_OF_PROCESSORS%  # Windows
   ```

3. **增量构建**: Lake 自动跟踪文件依赖，只重新构建变更文件

4. **选择性构建**:
   ```bash
   lake build MyProject.Module  # 只构建特定模块
   ```

5. **避免不必要的重新编译**:
   - 将大型 `import` 集中在根文件
   - 使用 `prelude` 减少导入开销
   - 分割大文件为多个小模块

### 4.4 诊断构建问题

```bash
# 查看详细输出
lake build --verbose

# 查看特定文件的构建
lake build --trace MyProject.File

# 查看构建图
lake build --watch  # 监视模式

# 检查 lake 状态
lake manifest  # 显示依赖清单
```

### 4.5 Lakefile 配置模板

```toml
# lakefile.toml - 推荐配置
name = "SylvaFormalization"
version = "0.1.0"
defaultTargets = ["SylvaFormalization"]

[leanOptions]
# 可读性选项
pp.unicode.fun = true        # 使用 Unicode 箭头 ↦
pp.proofs.withType = false   # 简化证明输出

# 性能选项
maxHeartbeats = 1000000      # 大文件需要更多时间

# 编译选项
# buildType = "Release"      # 发布模式（更快的运行时）

# 缓存配置 (v4.25.0+)
[cache]
remote = "https://reservoir.lean-lang.org/api/v1/cache"

[[require]]
name = "mathlib"
scope = "leanprover-community"
# 固定版本以保持一致性
rev = "v4.25.0"

[[lean_lib]]
name = "SylvaFormalization"

# 如果有可执行文件
# [[lean_exe]]
# name = "sylva"
# root = "Main"
```

---

## 5. Grind 战术系统深度解析

### 5.1 简介

`grind` 是 Lean 4 中的下一代自动证明策略，设计为 `simp` + `linarith` + 其他决策过程的组合式超级策略。

### 5.2 基本用法

```lean
example (a b c : Nat) : a + (b + c) = (a + b) + c := by grind

example [LE α] [Std.IsPreorder α] (a b c : α) : a ≤ b → b ≤ c → a ≤ c := by grind
```

### 5.3 交互模式 (v4.25.0+)

```lean
example : ... := by
  grind?        -- 生成可重现的战术脚本

-- 生成的脚本示例:
grind [intro h1, splitNext, cases? Nat, grind]
```

### 5.4 Grind 参数修饰符

```lean
-- 使用特定定理
grind [myTheorem]

-- 使用最小索引子表达式条件
grind [! -> myThm]

-- 使用默认模式推断
grind [default]
```

### 5.5 为 Grind 标注定理

```lean
-- 标记为 grind 简化规则
@[grind] theorem my_simp_rule : ...

-- 标记为单射定理
@[grind inj] theorem my_injective : ...

-- 使用旧版模式推断
@[grind!] theorem my_old_rule : ...
```

### 5.6 诊断与调试

```lean
set_option grind.debug true          -- 显示grind内部状态
set_option grind.trace true          -- 跟踪grind执行
set_option grind.param.codeAction true  -- 启用代码动作

-- 查看grind诊断信息
example : ... := by
  grind with diagnostics
```

### 5.7 Grind 能力矩阵

| 能力 | 状态 | 版本 |
|------|------|------|
| E-matching | ✅ 稳定 | v4.20+ |
| Linarith | ✅ 稳定 | v4.20+ |
| AC规范化 | ✅ 稳定 | v4.20+ |
| 模型组合(MBTC) | ✅ 稳定 | v4.21+ |
| 交换环(CommRing) | ✅ 稳定 | v4.22+ |
| 单射函数 | ✅ 稳定 | v4.25+ |
| 有序环/预序 | ✅ 稳定 | v4.25+ |
| 交互模式 | ✅ 稳定 | v4.25+ |
| 自动证明构造 | 🟡 改进中 | v4.25+ |

---

## 6. 已知问题速查表

### 6.1 编译/构建问题

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| PATH未配置 | 命令未找到 | 添加 `~/.elan/bin` 到 PATH |
| Unicode路径 | 编译失败 | 使用纯ASCII路径 |
| 版本不匹配 | `unknown package` | 检查 `lean-toolchain` 一致性 |
| 内存不足 | 编译崩溃 | 增加 `maxHeartbeats` |
| GitHub超时 | 下载失败 | 配置代理或手动下载 |
| 缓存过期 | 重新编译所有 | `lake clean && lake cache get` |

### 6.2 战术/证明问题

| 问题 | 解决方案 |
|------|----------|
| grind无限循环 | 添加 `with bounds` 限制 |
| simp不简化 | 检查是否导入了正确的simp集合 |
| 类型类推断失败 | 使用 `@` 显式提供实例 |
| 宇宙层级错误 | 使用 `Type*` 或显式指定宇宙 |

### 6.3 Mathlib特定问题

| 问题 | 解决方案 |
|------|----------|
| 模块已移除 | 检查mathlib更新日志，使用替代模块 |
| 命名变更 | 使用 `#find` 搜索新名称 |
| 依赖冲突 | 确保所有依赖使用相同lean版本 |

---

## 7. 参考链接汇总

### 官方资源

- **Lean 4 官方文档**: https://lean-lang.org/doc/reference/latest/
- **Lean 4 发布说明**: https://lean-lang.org/doc/reference/latest/releases/
- **Lean 4 GitHub**: https://github.com/leanprover/lean4
- **Elan (Lean版本管理器)**: https://github.com/leanprover/elan
- **Mathlib4 GitHub**: https://github.com/leanprover-community/mathlib4
- **Mathlib 概述**: https://leanprover-community.github.io/mathlib-overview.html

### 社区资源

- **Zulip 聊天**: https://leanprover.zulipchat.com/
  - `#lean4` 频道: 一般Lean 4讨论
  - `#mathlib4` 频道: Mathlib4特定讨论
  - `#new members` 频道: 新手求助
- **Lean Community 网站**: https://leanprover-community.github.io/
- **Mathlib API 文档**: https://leanprover-community.github.io/mathlib4_docs/

### Windows特定

- **Windows安装指南**: https://leanprover-community.github.io/install/windows.html
- **Elan Windows构建说明**: https://github.com/leanprover/elan#build-on-windows

### 教程与学习

- **Mathematics in Lean**: https://leanprover-community.github.io/mathematics_in_lean/
- **Functional Programming in Lean**: https://lean-lang.org/functional_programming_in_lean/
- **Theorem Proving in Lean 4**: https://lean-lang.org/theorem_proving_in_lean4/
- **Jesse Alama 的入门指南**: https://jessealama.net/articles/getting-started-with-lean-4/

### 活跃项目

- **Prime Number Theorem And**: https://github.com/AlexKontorovich/PrimeNumberTheoremAnd
- **Lean Goldbach**: https://github.com/topics/mathlib4 (搜索 Goldbach)
- **谱定理形式化**: https://github.com/leanprover-community/mathlib4 (相关PR)
- **可计算性学生项目**: https://git.abstractnonsen.se/max/mathlib4
- **CW-复形形式化**: Hannah Scholz 论文: http://florisvandoorn.com/theses/HannahScholz.pdf

### 学术参考

- **Math的未来形态**: https://arxiv.org/abs/2510.15924
- **HERALD数据集 (ICLR 2025)**: https://proceedings.iclr.cc/paper_files/paper/2025/file/8c2bb821410066459be64d03a4dc5719-Paper-Conference.pdf
- **几何代数形式化**: https://link.springer.com/content/pdf/10.1007/s00006-021-01164-1.pdf

### 特定技术参考

- **grind战术讨论**: https://proofassistants.stackexchange.com/questions/4953/what-is-the-grind-tactic-in-lean-4
- **Lean 4安装问题存档**: https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Lean.204.20installation.20issues.html
- **Lake文档**: https://lean-lang.org/doc/reference/latest/lake.html
- **Reservoir (包管理)**: https://reservoir.lean-lang.org/

---

## 附录 A: 快速诊断命令

```bash
# 环境检查清单
elan --version        # 应显示版本号
lake --version        # 应显示版本号
lean --version        # 应显示版本号

# 项目检查
cat lean-toolchain     # 检查toolchain版本
lake manifest          # 检查依赖清单
lake build --verbose   # 详细构建输出

# Mathlib特定
lake exe cache get     # 获取mathlib缓存
# 或 (v4.25.0+)
lake cache get

# 调试构建问题
lake clean             # 清理所有构建产物
rm -rf .lake/packages  # 强制重新下载依赖
lake update            # 重新获取依赖
lake build             # 重新构建
```

## 附录 B: Mathlib 维护者列表（按领域）

| 维护者 | 领域 |
|--------|------|
| Anne Baanen | 代数, 数论, 战术 |
| Kevin Buzzard | 代数, 数论, 代数几何 |
| Mario Carneiro | Lean形式化, 战术, 类型论 |
| Anatole Dedecker | 拓扑, 泛函分析, 微积分 |
| Rémy Degenne | 概率, 测度论, 分析 |
| Floris van Doorn | 测度论, 模型论, 战术 |
| Sébastien Gouëzel | 拓扑, 微积分, 几何, 分析 |
| Yury Kudryashov | 分析, 拓扑, 测度论 |
| Jireh Loreaux | 分析, 拓扑, 算子代数 |
| Patrick Massot | 文档, 拓扑, 几何 |
| Kim Morrison | 范畴论, 战术 |
| Oliver Nash | 代数, 几何, 拓扑 |
| Filippo Nuccio | 代数, 泛函分析, 同调, 数论 |
| Joël Riou | 范畴论, 同调, 代数几何 |
| Michael Rothgang | 微分几何, 分析, 拓扑 |

---

*本文档由 SYLVA 自动收集生成，最后更新: 2026-06-03*
*建议定期回访参考链接获取最新信息*
