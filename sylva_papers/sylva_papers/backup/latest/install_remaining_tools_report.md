# 剩余工具安装结果报告

**日期**: 2026-04-21
**环境**: Debian Trixie (ARM64), Python 3.13.5, Proot 容器

---

## 1. sagemath-standard

**状态**: ❌ 安装失败

**原因**: 
- sagemath-standard 依赖 `cypari2 >= 2.2.1`
- cypari2 依赖 `cysignals >= 1.11.3`
- cysignals 需要从源码编译 C 扩展
- 系统缺少 C++ 编译器 (`g++`/`c++`/`clang++`)

**错误日志**:
```
ERROR: Unknown compiler(s): [['c++'], ['g++'], ['clang++']]
Running `g++ --version` gave "[Errno 2] No such file or directory: 'g++'"
```

**根本原因**: 这是一个 Proot 容器环境，`dpkg` 无法创建备份文件 (`/var/lib/dpkg/status-old`)，导致无法通过 `apt` 安装 `g++` 和 `build-essential`。

---

## 2. cypari2 (PARI/GP 的 Python 接口)

**状态**: ❌ 安装失败

**原因**: 与 sagemath-standard 相同——缺少 C++ 编译器，无法编译 `cysignals` 依赖。

---

## 3. QuTiP (量子工具包)

**状态**: ❌ 安装失败

**原因**: 
- QuTiP 包含大量 Cython 扩展需要从源码编译
- 编译过程调用 `aarch64-linux-gnu-g++`，但该编译器不存在
- 错误: `command 'aarch64-linux-gnu-g++' failed: No such file or directory`

---

## 4. 替代方案: sympy

**状态**: ✅ 已安装 (v1.14.0)

**说明**: 
- sympy 是纯 Python 包，无需编译器
- 提供符号计算、代数、微积分、矩阵运算等功能
- 可作为 SageMath 的部分替代方案

---

## 5. 其他替代方案尝试

### PARI/GP (命令行工具)
**状态**: ❌ 无法通过 apt 安装
- `apt install pari-gp` 因 dpkg 权限问题失败

### GAP (群论软件)
**状态**: ❌ 无法通过 apt 安装
- `apt install gap` 因 dpkg 权限问题失败

---

## 总结

| 工具 | 状态 | 原因 |
|------|------|------|
| sagemath-standard | ❌ 失败 | 缺少 C++ 编译器 |
| cypari2 | ❌ 失败 | 缺少 C++ 编译器 |
| QuTiP | ❌ 失败 | 缺少 C++ 编译器 |
| sympy | ✅ 成功 | 纯 Python，无需编译 |
| PARI/GP (系统包) | ❌ 失败 | dpkg 权限限制 |
| GAP (系统包) | ❌ 失败 | dpkg 权限限制 |

**核心阻塞**: Proot 容器环境中 `dpkg` 无法创建备份文件，导致无法安装任何需要编译的系统级工具（g++、build-essential）。

**建议**:
1. 如果可能，在非 Proot 环境（如 Docker 或原生 Linux）中运行安装
2. 或手动下载并解压编译器二进制文件到 PATH 中（已尝试提取 .deb 包但缺少完整依赖链）
3. 目前 sympy 是唯一可用的符号计算工具
