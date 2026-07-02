# PFE 引用 TOE-SYLVA 核心形式化

本目录不直接包含形式化代码，而是**引用** [TOE-SYLVA](https://github.com/yimeng2026/TOE-SYLVA) 的核心模块。

## 引用规则

PFE 作为工程应用分支，不直接修改 TOE-SYLVA 的学术形式化代码。所有修改在 TOE-SYLVA 主仓库完成，PFE 通过以下方式引用：

### 1. 只读引用（数值验证）

PFE 的 `sagemath_verification/` 脚本读取 TOE-SYLVA 的 Lean 代码中的数学定义，转化为数值验证算法。

### 2. 状态同步（代理分析）

PFE 通过千界花园的 `POST /api/research/sylva-sync` 接口获取 TOE-SYLVA 的最新状态：
- 模块列表和编译状态
- 开放问题（sorry）分布
- 定理层次结构

### 3. 工程启发（反向反馈）

PFE 的数值实验结果可以启发 TOE-SYLVA 的定理方向：
- 数值验证成功 → 指导 TOE-SYLVA 优先证明该方向
- 数值反例发现 → 指导 TOE-SYLVA 修正定理边界条件
- 物理预言 → 为 TOE-SYLVA 提供新的公理化方向

## 本地同步方法

```bash
# 从 TOE-SYLVA 拉取最新形式化代码
# 但不直接编辑，只做数值验证和工程实验

cd sylva-release/src/
# 使用 Lean 文件作为数值验证的输入规范
# 使用 Python/SageMath 执行验证
```

## 引用状态

| 模块 | 引用版本 | 工程用途 |
|------|---------|---------|
| BSD.lean | v5.32 | 椭圆曲线约化验证、秩计算验证 |
| DynamicalSystem.lean | v5.32 | 动力系统因子检测 |
| RiemannHypothesis.lean | v5.32 | ζ函数零点数值验证 |
| Complexity.lean | v5.32 | SAT 求解器复杂度基准测试 |
| NavierStokes.lean | v5.32 | 流体模拟验证 |

---

**注意**：PFE 的 `sylva-release/` 目录不应包含直接修改的 `.lean` 文件。所有形式化修改应在 [TOE-SYLVA](https://github.com/yimeng2026/TOE-SYLVA) 中完成，通过 Git 同步后 PFE 引用。
