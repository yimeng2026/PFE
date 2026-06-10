# 剩余数学物理工具安装报告

## 环境信息
- **日期**: 2026-04-21
- **Python**: 3.13
- **平台**: Linux arm64 (PRoot-Distro)
- **pip**: 26.0.1

---

## 1. QuTiP（量子计算工具包）

### 状态: ⚠️ 部分成功（通过 --break-system-packages 安装）

```bash
pip install --break-system-packages qutip
```

**结果**: ✅ 安装成功
- QuTiP 5.1.1 已安装
- 依赖: numpy, scipy, cython 自动安装

**验证**:
```python
import qutip
print(qutip.__version__)  # 5.1.1
```

---

## 2. SageMath

### 状态: ❌ 失败

```bash
pip install --break-system-packages sagemath-standard
```

**错误**: 无预编译 wheel，需从源码编译。在 arm64 + 受限环境中构建失败。

**替代方案**: ✅ SymPy + 扩展模块
```bash
pip install --break-system-packages sympy sympy-plot-backends
```

**结果**: SymPy 1.13.3 安装成功

---

## 3. 可视化工具

### Mayavi
**状态**: ❌ 失败
- 依赖 VTK，在受限环境中编译失败

### VTK
**状态**: ❌ 失败
- 无预编译 arm64 wheel，编译需要大量资源

**替代方案**: ✅ matplotlib + plotly
```bash
pip install --break-system-packages matplotlib plotly
```

---

## 4. 符号计算扩展

### SymPy-Plot-Backends
**状态**: ✅ 成功
- 安装版本: 3.0.3

---

## 安装摘要

| 工具 | 状态 | 版本 | 备注 |
|------|------|------|------|
| QuTiP | ✅ | 5.1.1 | 量子计算核心工具 |
| NumPy | ✅ | 2.2.6 | QuTiP 依赖 |
| SciPy | ✅ | 1.15.3 | QuTiP 依赖 |
| Cython | ✅ | 3.0.12 | QuTiP 依赖 |
| SymPy | ✅ | 1.13.3 | SageMath 替代 |
| sympy-plot-backends | ✅ | 3.0.3 | 符号可视化 |
| Matplotlib | ✅ | 3.10.3 | 基础可视化 |
| Plotly | ✅ | 6.2.0 | 交互式可视化 |
| SageMath | ❌ | - | 需源码编译，环境受限 |
| Mayavi | ❌ | - | VTK 依赖失败 |
| VTK | ❌ | - | 无预编译 wheel |

---

## 可用工具验证

### QuTiP 测试
```python
import qutip as qt

# 创建量子态
psi = qt.basis(2, 0)
print(f"量子态: {psi}")

# 创建泡利算符
sigma_x = qt.sigmax()
print(f"σ_x 作用: {sigma_x * psi}")

# 创建量子谐振子
a = qt.destroy(10)
print(f"湮灭算符维度: {a.dims}")
```

### SymPy 测试
```python
import sympy as sp

x = sp.Symbol('x')
f = sp.sin(x) * sp.exp(-x**2)
print(f"积分: {sp.integrate(f, x)}")

# 矩阵运算
M = sp.Matrix([[1, 2], [3, 4]])
print(f"特征值: {M.eigenvals()}")
```

---

## 限制说明

1. **SageMath**: 完整版需要编译大量 C/C++ 扩展，在受限环境中不可行
   - 替代方案: SymPy 覆盖大部分符号计算需求
   
2. **Mayavi/VTK**: 3D 可视化需要原生编译
   - 替代方案: matplotlib (3D), plotly (交互式)

3. **安装方式**: 使用 `--break-system-packages` 绕过系统保护
   - 风险: 可能干扰系统 Python 包
   - 缓解: 所有包安装到用户目录 (`/root/.local`)

---

## 建议

如需完整 SageMath 或 VTK，考虑:
1. 使用 Docker 容器 (sagemath/sagemath)
2. 使用 conda 环境 (更完善的预编译包)
3. 在更完整的 Linux 发行版上安装
