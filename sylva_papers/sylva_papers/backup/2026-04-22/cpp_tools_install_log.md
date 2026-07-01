# C++ 编译器和剩余工具安装记录

## 1. C++ 编译器 (gcc/g++)

- **gcc**: ✅ 已安装 (Debian 14.2.0-19, 14.2.0)
- **g++**: ✅ 已安装 (Debian 14.2.0-19, 14.2.0)
- **状态**: 完成

---

## 2. PARI/GP

- **状态**: ✅ 已安装
- **版本**: 2.17.2-1
- **验证**: `gp -q -f` 运行正常

---

## 3. GAP

- **状态**: ✅ 已安装
- **版本**: 4.14.0-3
- **验证**: `gap -q -b` 运行正常，输出 "GAP test OK"

---

## 4. Python 科学计算工具

### 4.1 QuTiP
- **状态**: ❌ 安装失败
- **原因**: 缺少 Python 开发头文件 (`Python.h: No such file or directory`)
- **解决方案**: 需要安装 `python3-dev` 包

### 4.2 sympy
- **状态**: ❌ 未安装（QuTiP 构建失败导致 pip 中断）
- **解决方案**: 安装 `python3-dev` 后重试，或使用 `apt-get install python3-sympy`

---

## 5. SageMath

- **状态**: ⚠️ 未安装
- **替代方案**: 使用 `sympy` 作为替代
- **说明**: SageMath 是大型软件包，在容器环境中安装困难。`sympy` 提供符号数学计算功能

---

## 6. 安装问题汇总

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| dpkg status-old 权限错误 | 容器环境限制 | 已绕过，手动管理 status 文件 |
| Python.h 缺失 | python3-dev 未安装 | `apt-get install python3-dev` |
| 外部管理环境 | PEP 668 限制 | 使用 `--break-system-packages` |

---

## 7. 后续步骤

1. 安装 `python3-dev` 以支持 QuTiP 编译
2. 重试安装 QuTiP 和 sympy
3. 考虑使用 `apt-get install python3-sympy` 作为备选

---

## 8. 已安装工具清单

- ✅ gcc (14.2.0)
- ✅ g++ (14.2.0)
- ✅ PARI/GP (2.17.2)
- ✅ GAP (4.14.0)
- ❌ QuTiP (需 python3-dev)
- ❌ sympy (需重试)
- ⚠️ SageMath (使用 sympy 替代)
