"""
Level Ontology — Seven-Layer Emergence Ontology
七层涌现本体论

参考：TOE-SYLVA 05_FourForcesUnification_Formalization_Fixed.lean 中的 Level 定义

PFE 七层能量标度（从微观到宏观）：

L1: 普朗克尺度 (Planck Scale) — 10^-35 m
L2: 量子场论 (QFT) — 10^-15 m
L3: 原子/分子 (Atomic) — 10^-10 m
L4: 经典物理 (Classical) — 10^0 m
L5: 生物/化学 (Biochemical) — 10^2 m
L6: 社会/经济 (Socioeconomic) — 10^6 m
L7: 宇宙学 (Cosmological) — 10^26 m

层间耦合规则：
- 相邻层级的耦合强度 ∝ 1/φ
- 跨层级的耦合强度 ∝ 1/φ^|L_i - L_j|
- 涌现公式：Mass(L_{n+1}) = f(Void(L_n), coupling(L_n, L_{n+1}))
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Dict, List, Optional, Tuple, Union

from .phi_engine import PHI, PhiEngine


# ============================================================
# SECTION 1: EMERGENCE LEVEL ENUM
# ============================================================

class EmergenceLevel(Enum):
    """
    七层涌现层级。

    每个层级对应不同的能量标度和物理/工程领域。
    """
    L1_PLANCK = 1        # 普朗克尺度: 10^-35 m, 10^19 GeV
    L2_QFT = 2           # 量子场论: 10^-15 m, 10^2 GeV
    L3_ATOMIC = 3        # 原子/分子: 10^-10 m, 1 eV
    L4_CLASSICAL = 4     # 经典物理: 10^0 m, 1 J
    L5_BIOCHEMICAL = 5   # 生物/化学: 10^2 m, 10^3 J
    L6_SOCIOECONOMIC = 6 # 社会/经济: 10^6 m, 10^12 J
    L7_COSMOLOGICAL = 7  # 宇宙学: 10^26 m, 10^50 J

    def scale_factor(self) -> float:
        """返回层级的标度因子（相对于 L1）"""
        return PHI ** (self.value - 1)

    def description(self) -> str:
        descriptions = {
            EmergenceLevel.L1_PLANCK: "Planck Scale — Quantum Gravity",
            EmergenceLevel.L2_QFT: "Quantum Field Theory — Standard Model",
            EmergenceLevel.L3_ATOMIC: "Atomic & Molecular — Chemistry",
            EmergenceLevel.L4_CLASSICAL: "Classical Physics — Engineering",
            EmergenceLevel.L5_BIOCHEMICAL: "Biochemical & Living Systems",
            EmergenceLevel.L6_SOCIOECONOMIC: "Socioeconomic & Complex Networks",
            EmergenceLevel.L7_COSMOLOGICAL: "Cosmological & Universe Scale",
        }
        return descriptions.get(self, "Unknown")

    def __repr__(self) -> str:
        return f"{self.name}(scale={self.scale_factor():.4f})"


# ============================================================
# SECTION 2: LEVEL COUPLING
# ============================================================

@dataclass
class LevelCoupling:
    """
    层间耦合规则。

    coupling_strength(L_i, L_j) = base_coupling * φ^(-|i-j|)

    相邻层级的耦合最强（φ^(-1) ≈ 0.618），
    跨层级耦合随距离指数衰减。
    """

    from_level: EmergenceLevel
    to_level: EmergenceLevel
    base_coupling: float = 1.0
    coupling_function: Optional[Callable[[float], float]] = None

    def strength(self) -> float:
        """计算耦合强度"""
        distance = abs(self.from_level.value - self.to_level.value)
        raw = self.base_coupling * (PHI ** (-distance))
        if self.coupling_function:
            return self.coupling_function(raw)
        return raw

    def __repr__(self) -> str:
        return f"LevelCoupling({self.from_level.name} → {self.to_level.name}, strength={self.strength():.6f})"


# ============================================================
# SECTION 3: LEVEL ONTOLOGY ENGINE
# ============================================================

class LevelOntology:
    """
    七层涌现本体论引擎。

    核心功能：
    1. 管理七层标度结构
    2. 计算层间耦合
    3. 执行跨层级涌现
    4. 评估涌现的层级一致性

    涌现公式（层间映射）：
        Mass(L_{n+1}) = EmergenceRule(Void(L_n)) × coupling(L_n, L_{n+1})
    """

    def __init__(self, base_coupling: float = 1.0):
        self.base_coupling = base_coupling
        self._couplings: Dict[Tuple[EmergenceLevel, EmergenceLevel], LevelCoupling] = {}
        self._initialize_couplings()

    def _initialize_couplings(self) -> None:
        """初始化所有层间耦合"""
        levels = list(EmergenceLevel)
        for i, li in enumerate(levels):
            for j, lj in enumerate(levels):
                if i != j:
                    self._couplings[(li, lj)] = LevelCoupling(
                        from_level=li,
                        to_level=lj,
                        base_coupling=self.base_coupling,
                    )

    def get_coupling(self, from_level: EmergenceLevel, to_level: EmergenceLevel) -> LevelCoupling:
        """获取两个层级之间的耦合"""
        return self._couplings.get((from_level, to_level), LevelCoupling(from_level, to_level))

    def get_adjacent_couplings(self, level: EmergenceLevel) -> List[LevelCoupling]:
        """获取相邻层级的耦合（上和下）"""
        levels = list(EmergenceLevel)
        idx = level.value - 1
        result = []
        if idx > 0:
            result.append(self.get_coupling(levels[idx - 1], level))
            result.append(self.get_coupling(level, levels[idx - 1]))
        if idx < len(levels) - 1:
            result.append(self.get_coupling(levels[idx + 1], level))
            result.append(self.get_coupling(level, levels[idx + 1]))
        return result

    def cross_level_emergence(
        self,
        void_value: float,
        from_level: EmergenceLevel,
        to_level: EmergenceLevel,
        emergence_rule: Optional[Callable[[float, float], float]] = None,
    ) -> float:
        """
        跨层级涌现计算。

        默认规则：mass = void_value × coupling_strength × scale_factor_ratio
        """
        coupling = self.get_coupling(from_level, to_level)
        c = coupling.strength()
        scale_ratio = to_level.scale_factor() / from_level.scale_factor()

        if emergence_rule:
            return emergence_rule(void_value, c * scale_ratio)

        return void_value * c * scale_ratio

    def multi_level_emergence(
        self,
        void_values: Dict[EmergenceLevel, float],
        target_level: EmergenceLevel,
    ) -> float:
        """
        多层级综合涌现。

        从多个源层级综合涌现到目标层级，使用加权平均。
        """
        contributions = []
        weights = []
        for source_level, void_val in void_values.items():
            if source_level == target_level:
                continue
            mass = self.cross_level_emergence(void_val, source_level, target_level)
            coupling = self.get_coupling(source_level, target_level)
            weight = coupling.strength()
            contributions.append(mass * weight)
            weights.append(weight)

        if not weights or sum(weights) == 0:
            return void_values.get(target_level, 0.0)

        return sum(contributions) / sum(weights)

    def level_consistency_score(
        self,
        values: Dict[EmergenceLevel, float],
    ) -> float:
        """
        评估跨层级值的一致性。

        如果相邻层级的值符合 φ 标度律，则一致性高。
        返回 0.0 - 1.0 的评分。
        """
        levels = sorted(values.keys(), key=lambda l: l.value)
        if len(levels) < 2:
            return 1.0

        scores = []
        for i in range(len(levels) - 1):
            l1, l2 = levels[i], levels[i + 1]
            v1, v2 = values[l1], values[l2]
            expected_ratio = l2.scale_factor() / l1.scale_factor()
            actual_ratio = v2 / v1 if v1 != 0 else 0.0
            if expected_ratio > 0 and actual_ratio > 0:
                log_ratio = math.log(actual_ratio) / math.log(expected_ratio)
                error = abs(log_ratio - 1.0)
                score = max(0.0, 1.0 - error)
                scores.append(score)

        return sum(scores) / len(scores) if scores else 0.0

    def __repr__(self) -> str:
        return f"LevelOntology(base_coupling={self.base_coupling})"


# ============================================================
# SECTION 4: SCALE CONSTANTS
# ============================================================

# 七层标度的典型物理量（仅供参考）
LEVEL_SCALE_METERS: Dict[EmergenceLevel, float] = {
    EmergenceLevel.L1_PLANCK: 1.616e-35,
    EmergenceLevel.L2_QFT: 1e-15,
    EmergenceLevel.L3_ATOMIC: 5.29e-11,
    EmergenceLevel.L4_CLASSICAL: 1.0,
    EmergenceLevel.L5_BIOCHEMICAL: 1e2,
    EmergenceLevel.L6_SOCIOECONOMIC: 1e6,
    EmergenceLevel.L7_COSMOLOGICAL: 8.8e26,
}

LEVEL_SCALE_ENERGY: Dict[EmergenceLevel, float] = {
    EmergenceLevel.L1_PLANCK: 1.22e19,  # GeV
    EmergenceLevel.L2_QFT: 1e2,       # GeV
    EmergenceLevel.L3_ATOMIC: 1e-9,   # GeV (1 eV ≈ 1e-9 GeV)
    EmergenceLevel.L4_CLASSICAL: 6.24e9, # GeV (1 J)
    EmergenceLevel.L5_BIOCHEMICAL: 6.24e12,
    EmergenceLevel.L6_SOCIOECONOMIC: 6.24e21,
    EmergenceLevel.L7_COSMOLOGICAL: 6.24e59,
}


# ============================================================
# SECTION 5: UTILITY FUNCTIONS
# ============================================================

def level_from_scale(meters: float) -> EmergenceLevel:
    """根据尺度（米）推断最接近的层级"""
    best_level = EmergenceLevel.L4_CLASSICAL
    best_error = float('inf')
    for level, scale in LEVEL_SCALE_METERS.items():
        if scale > 0 and meters > 0:
            error = abs(math.log(meters / scale))
            if error < best_error:
                best_error = error
                best_level = level
    return best_level


def demo():
    """七层涌现本体论演示"""
    print("=" * 60)
    print("Level Ontology — Seven-Layer Emergence Engine Demo")
    print("=" * 60)

    print(f"\n[Levels]")
    for level in EmergenceLevel:
        print(f"  {level.name}: scale_factor={level.scale_factor():.4f}")
        print(f"    {level.description()}")
        print(f"    ~{LEVEL_SCALE_METERS[level]:.2e} m, ~{LEVEL_SCALE_ENERGY[level]:.2e} GeV")

    print(f"\n[Couplings]")
    ontology = LevelOntology(base_coupling=1.0)
    for level in EmergenceLevel:
        adj = ontology.get_adjacent_couplings(level)
        print(f"  {level.name}:")
        for c in adj:
            print(f"    {c.from_level.name} ↔ {c.to_level.name}: strength={c.strength():.6f}")

    print(f"\n[Cross-Level Emergence]")
    # 从 L2 (QFT) 涌现到 L3 (Atomic)
    void_qft = 100.0  # 某个 QFT 量
    mass_atomic = ontology.cross_level_emergence(void_qft, EmergenceLevel.L2_QFT, EmergenceLevel.L3_ATOMIC)
    print(f"  void(L2_QFT)={void_qft} → mass(L3_ATOMIC)={mass_atomic:.6f}")

    # 从 L3 (Atomic) 涌现到 L4 (Classical)
    void_atomic = 1.0
    mass_classical = ontology.cross_level_emergence(void_atomic, EmergenceLevel.L3_ATOMIC, EmergenceLevel.L4_CLASSICAL)
    print(f"  void(L3_ATOMIC)={void_atomic} → mass(L4_CLASSICAL)={mass_classical:.6f}")

    print(f"\n[Multi-Level Emergence]")
    void_values = {
        EmergenceLevel.L2_QFT: 100.0,
        EmergenceLevel.L3_ATOMIC: 1.0,
    }
    target = EmergenceLevel.L4_CLASSICAL
    multi_mass = ontology.multi_level_emergence(void_values, target)
    print(f"  Multi-source → mass(L4_CLASSICAL)={multi_mass:.6f}")

    print(f"\n[Consistency Score]")
    values = {
        EmergenceLevel.L1_PLANCK: 1.0,
        EmergenceLevel.L2_QFT: PHI,
        EmergenceLevel.L3_ATOMIC: PHI ** 2,
        EmergenceLevel.L4_CLASSICAL: PHI ** 3,
    }
    score = ontology.level_consistency_score(values)
    print(f"  Consistency score (φ-scaled): {score:.4f}")

    inconsistent_values = {
        EmergenceLevel.L1_PLANCK: 1.0,
        EmergenceLevel.L2_QFT: 2.0,
        EmergenceLevel.L3_ATOMIC: 100.0,
    }
    score2 = ontology.level_consistency_score(inconsistent_values)
    print(f"  Consistency score (random): {score2:.4f}")

    return ontology


if __name__ == "__main__":
    demo()
