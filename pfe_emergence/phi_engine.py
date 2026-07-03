"""
Phi Engine — Golden Ratio φ Self-Similar Emergence Engine
黄金比例 φ 涌现引擎

参考：TOE-SYLVA sylva_complete/Basic.lean 中的 φ 定义和性质

φ = (1 + √5) / 2 ≈ 1.6180339887...

φ 的核心性质：
- φ² = φ + 1
- 1/φ = φ - 1
- φ 是 Fibonacci 序列的极限比值
- Binet 公式: F_n = (φ^n - φ̄^n) / √5

在 Sylva/EmergentMath 中，φ 被视为"涌现数学"的原型：
它跨越数学、物理、生物多个领域，代表物理约束与数学结构之间的
基本共振。
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterator, List, Optional, Tuple, Union


# ============================================================
# SECTION 1: φ CONSTANTS & BASIC PROPERTIES
# ============================================================

PHI: float = (1 + math.sqrt(5)) / 2
"""黄金比例 φ ≈ 1.6180339887..."""

PHI_CONJUGATE: float = (1 - math.sqrt(5)) / 2
"""φ 的共轭 ≈ -0.6180339887... = 1 - φ"""

PHI_INV: float = 1 / PHI
"""1/φ = φ - 1 ≈ 0.6180339887..."""


def fibonacci(n: int) -> int:
    """
    Fibonacci 数列。
    F_0 = 0, F_1 = 1, F_n = F_{n-1} + F_{n-2}
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def binet_formula(n: int) -> float:
    """
    Binet 公式：F_n = (φ^n - φ̄^n) / √5

    参考：TOE-SYLVA Basic.lean theorem binet_formula
    """
    return (PHI ** n - PHI_CONJUGATE ** n) / math.sqrt(5)


def phi_powers(n_max: int) -> Iterator[Tuple[int, float]]:
    """生成 φ^n 序列，展示自相似性"""
    for n in range(n_max + 1):
        yield n, PHI ** n


# ============================================================
# SECTION 2: SELF-SIMILAR EMERGENCE
# ============================================================

@dataclass
class SelfSimilarEmergence:
    """
    自相似涌现结构。

    基于 φ 的自相似性：
    - 每个尺度 level n 的结构与 level n-1 和 n-2 的结构相关
    - 尺度因子遵循 φ 的幂律
    - 涌现量 = 前两个尺度涌现量的和（Fibonacci 递归）
    """

    base_value: float = 1.0
    scale_factor: float = PHI
    levels: List[float] = field(default_factory=list)
    _metadata: Dict[str, any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.levels:
            self.levels = [self.base_value]

    def evolve(self, steps: int = 1) -> None:
        """
        推进自相似涌现。

        规则：level[n] = level[n-1] + level[n-2]
        （Fibonacci 递归，但应用于任意涌现量）
        """
        for _ in range(steps):
            if len(self.levels) == 1:
                next_val = self.levels[0] * self.scale_factor
            else:
                next_val = self.levels[-1] + self.levels[-2]
            self.levels.append(next_val)

    def ratio(self, level: int) -> float:
        """返回相邻层级比值"""
        if level <= 0 or level >= len(self.levels):
            return float('nan')
        return self.levels[level] / self.levels[level - 1]

    def convergence_to_phi(self, tolerance: float = 1e-6) -> Optional[int]:
        """
        找到比值收敛到 φ 的层级。

        返回收敛发生的层级索引，或 None 如果未收敛。
        """
        for i in range(1, len(self.levels)):
            r = self.ratio(i)
            if abs(r - PHI) < tolerance:
                return i
        return None

    def __len__(self) -> int:
        return len(self.levels)

    def __getitem__(self, idx: int) -> float:
        return self.levels[idx]

    def __repr__(self) -> str:
        return f"SelfSimilarEmergence(levels={len(self.levels)}, base={self.base_value:.4f})"


# ============================================================
# SECTION 3: PHI ENGINE — 主引擎
# ============================================================

class PhiEngine:
    """
    黄金比例 φ 涌现引擎。

    核心功能：
    1. 生成 φ 自相似序列
    2. 计算 φ 相关物理量的涌现值
    3. 提供 φ 的数值近似和精确公式

    PFE 工程应用：
    - 作为涌现量级的尺度基准
    - 用于评估涌现结果的"自然性"（偏离 φ 的度量）
    - 作为层间耦合的标度因子
    """

    def __init__(self, precision: int = 15):
        self.precision = precision
        self._phi_approx = self._compute_phi(precision)

    @staticmethod
    def _compute_phi(iterations: int) -> float:
        """通过连分数计算 φ 的近似值"""
        # φ = [1; 1, 1, 1, ...] 连分数
        result = 1.0
        for _ in range(iterations):
            result = 1 + 1 / result
        return result

    def phi_value(self) -> float:
        """返回 φ 的精确值（使用 math.sqrt）"""
        return PHI

    def phi_approximation(self) -> float:
        """返回 φ 的近似值（使用连分数）"""
        return self._phi_approx

    def generate_sequence(self, n: int, base: float = 1.0) -> List[float]:
        """生成 φ 自相似序列：a_n = a_{n-1} + a_{n-2}"""
        seq = [base, base * PHI]
        for i in range(2, n):
            seq.append(seq[i - 1] + seq[i - 2])
        return seq[:n]

    def golden_spiral_points(self, n_points: int, radius: float = 1.0) -> List[Tuple[float, float]]:
        """
        生成黄金螺旋上的点。

        极坐标：r = a * e^(bθ), b = ln(φ) / (π/2)
        """
        b = math.log(PHI) / (math.pi / 2)
        points = []
        for i in range(n_points):
            theta = i * 2 * math.pi / PHI  # 黄金角
            r = radius * math.exp(b * theta)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.append((x, y))
        return points

    def naturality_score(self, value: float, expected_scale: float = 1.0) -> float:
        """
        计算值的"自然性"评分。

        如果 value / expected_scale 接近 φ 的幂，则评分高。
        返回 0.0 - 1.0 的评分，1.0 表示"最自然"。
        """
        ratio = value / expected_scale
        if ratio <= 0:
            return 0.0
        log_ratio = math.log(ratio) / math.log(PHI)
        distance_from_nearest_phi_power = abs(log_ratio - round(log_ratio))
        return max(0.0, 1.0 - distance_from_nearest_phi_power)

    def resonance_frequency(self, base_freq: float) -> List[float]:
        """
        计算 φ 共振频率序列。

        f_n = base_freq * φ^n，n = 0, ±1, ±2, ...
        """
        return [base_freq * (PHI ** n) for n in range(-3, 4)]

    def __repr__(self) -> str:
        return f"PhiEngine(precision={self.precision}, phi={self.phi_value():.10f})"


# ============================================================
# SECTION 4: UTILITY FUNCTIONS
# ============================================================

def is_phi_power(value: float, tolerance: float = 1e-3) -> bool:
    """检查值是否接近 φ 的整数幂"""
    if value <= 0:
        return False
    log_val = math.log(value) / math.log(PHI)
    return abs(log_val - round(log_val)) < tolerance


def phi_power_index(value: float) -> Optional[int]:
    """返回值最接近的 φ 幂指数"""
    if value <= 0:
        return None
    log_val = math.log(value) / math.log(PHI)
    return round(log_val)


def demo():
    """φ 引擎演示"""
    print("=" * 60)
    print("Phi Engine — Golden Ratio Self-Similar Emergence Demo")
    print("=" * 60)

    print(f"\n[Constants]")
    print(f"  φ = {PHI:.15f}")
    print(f"  φ̄ = {PHI_CONJUGATE:.15f}")
    print(f"  1/φ = {PHI_INV:.15f}")
    print(f"  φ - 1 = {PHI - 1:.15f}")
    print(f"  φ² = {PHI ** 2:.15f}")
    print(f"  φ + 1 = {PHI + 1:.15f}")
    print(f"  φ² == φ + 1 ? {abs(PHI ** 2 - (PHI + 1)) < 1e-12}")

    print(f"\n[Fibonacci]")
    for n in range(15):
        fib = fibonacci(n)
        binet = binet_formula(n)
        print(f"  F_{n:2d} = {fib:4d} (Binet: {binet:.2f})")

    print(f"\n[Self-Similar Emergence]")
    emergence = SelfSimilarEmergence(base_value=1.0)
    emergence.evolve(steps=20)
    for i in range(1, min(15, len(emergence.levels))):
        r = emergence.ratio(i)
        print(f"  Level {i:2d}: {emergence.levels[i]:10.4f}, ratio={r:.10f}, |r-φ|={abs(r-PHI):.2e}")

    conv = emergence.convergence_to_phi(tolerance=1e-6)
    print(f"  Convergence to φ at level: {conv}")

    print(f"\n[Phi Engine]")
    engine = PhiEngine(precision=20)
    print(f"  {engine}")
    print(f"  Approximation error: {abs(engine.phi_approximation() - PHI):.2e}")

    print(f"\n[Naturality Score]")
    test_values = [1.0, PHI, PHI ** 2, 2.0, 3.14159, PHI * 1.001]
    for v in test_values:
        score = engine.naturality_score(v)
        print(f"  {v:.6f}: naturality={score:.4f}")

    print(f"\n[Resonance Frequencies]")
    freqs = engine.resonance_frequency(base_freq=440.0)
    for i, f in enumerate(freqs):
        print(f"  f_{i-3:2d}: {f:.2f} Hz")

    return engine


if __name__ == "__main__":
    demo()
