"""
ZhiKong Mass-Void Theory Core Engine
质空论核心引擎

参考：PFE_MANIFESTO.md Section 5 — PFE 的"质空论"工程实践

| 质空论维度 | 学术表达（TOE-SYLVA） | 工程表达（PFE） |
|-----------|---------------------|---------------|
| 质 | 定理、证明、严格形式化 | 数值拟合、计算验证、行业部署、LLM 代理、自动化管道 |
| 空 | 公理、假设、抽象结构 | 因果网络拓扑、数据流图、拓扑涌现、抽象框架、反模式 |
| 涌现 | 从公理到定理的推导 | 从数据到模型的拟合、从拓扑到物理量的涌现、从空到质的自动化 |
"""

from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Protocol, Set, Tuple, Union


# ============================================================
# SECTION 1: ABSTRACT BASE CLASSES — Void & Mass
# ============================================================

class Void(ABC):
    """
    空 (Void) — 抽象拓扑结构、因果网络、数学框架。

    Void 是涌现的"原材料"：它不是物理量，而是物理量得以涌现的结构基础。
    在 PFE 中，Void 可以是因果网络、数据流图、拓扑空间、抽象代数结构。
    """

    @abstractmethod
    def topology(self) -> Dict[str, Any]:
        """返回 Void 的拓扑描述（节点、边、连通性等）"""
        pass

    @abstractmethod
    def dimension(self) -> int:
        """返回 Void 的拓扑维度"""
        pass

    @abstractmethod
    def connectivity(self, node_id: Union[int, str]) -> float:
        """返回指定节点的连通性度量"""
        pass

    def __repr__(self) -> str:
        return f"Void(dim={self.dimension()})"


class Mass(ABC):
    """
    质 (Mass) — 可测量、可验证的物理量或工程输出。

    Mass 是涌现的"产物"：它是从 Void 结构中提取出的可量化、可验证的数值。
    在 PFE 中，Mass 可以是物理常数、数值结果、工程指标、LLM 输出质量评分。
    """

    @abstractmethod
    def value(self) -> float:
        """返回 Mass 的数值表示"""
        pass

    @abstractmethod
    def uncertainty(self) -> float:
        """返回 Mass 的测量/计算不确定性"""
        pass

    @abstractmethod
    def confidence(self) -> float:
        """返回 Mass 的可信度（0.0 - 1.0）"""
        pass

    def __repr__(self) -> str:
        return f"Mass(v={self.value():.6f}, σ={self.uncertainty():.6f}, c={self.confidence():.3f})"


# ============================================================
# SECTION 2: EMERGENCE RULE — Void → Mass 映射
# ============================================================

class EmergenceRule(ABC):
    """
    涌现规则 (Emergence Rule) — 从 Void 拓扑网络生成 Mass 物理量的规则。

    涌现规则是质空论的核心：它定义了"空"如何转化为"质"。
    PFE 的涌现不追求数学严格性，而是追求"有效涌现"——
    通过数值拟合、启发式、近似计算让抽象结构涌现出可验证的结果。
    """

    @abstractmethod
    def apply(self, void: Void) -> Mass:
        """将 Void 拓扑映射为 Mass 物理量"""
        pass

    @abstractmethod
    def name(self) -> str:
        """规则名称"""
        pass

    @abstractmethod
    def description(self) -> str:
        """规则描述"""
        pass

    def __repr__(self) -> str:
        return f"EmergenceRule({self.name()})"


# ============================================================
# SECTION 3: CONVERGENCE CRITERION — 有效涌现判定
# ============================================================

class ConvergenceCriterion(ABC):
    """
    收敛准则 (Convergence Criterion) — 判定涌现是否"有效"的标准。

    PFE 的有效涌现判定基于工程实用性而非数学严格性：
    - 数值稳定性：结果对输入扰动的鲁棒性
    - 可复现性：多次运行结果的一致性
    - 物理合理性：结果与已知物理定律的兼容性
    - 预测能力：结果对未知现象的预言能力
    """

    @abstractmethod
    def evaluate(self, mass: Mass, history: List[Mass]) -> bool:
        """
        评估当前 Mass 是否满足收敛准则。

        Args:
            mass: 当前涌现的 Mass
            history: 历史涌现结果（用于判断稳定性）

        Returns:
            True 如果涌现有效，False 否则
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """准则名称"""
        pass

    def __repr__(self) -> str:
        return f"ConvergenceCriterion({self.name()})"


# ============================================================
# SECTION 4: CONCRETE IMPLEMENTATIONS
# ============================================================

@dataclass
class SimpleVoid(Void):
    """
    简单 Void 实现：基于邻接表的拓扑网络。

    参考：alpha_derivation/01_causal_network_simulation.py 中的 CausalNetwork
    """

    nodes: List[int] = field(default_factory=list)
    edges: List[Tuple[int, int]] = field(default_factory=list)
    weights: Dict[Tuple[int, int], float] = field(default_factory=dict)
    node_positions: Dict[int, Tuple[float, ...]] = field(default_factory=dict)
    _dim: int = 4

    def topology(self) -> Dict[str, Any]:
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "average_degree": self._average_degree(),
            "dimension": self._dim,
        }

    def dimension(self) -> int:
        return self._dim

    def connectivity(self, node_id: Union[int, str]) -> float:
        """Return the weighted degree, counting each incident edge once."""
        nid = int(node_id)
        weighted = 0.0
        for u, v in self.edges:
            if nid == u or nid == v:
                key = (min(u, v), max(u, v))
                weighted += self.weights.get(key, 1.0)
        return weighted

    def _average_degree(self) -> float:
        if not self.nodes:
            return 0.0
        return 2.0 * len(self.edges) / len(self.nodes)

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        self.edges.append((u, v))
        self.weights[(min(u, v), max(u, v))] = weight

    @classmethod
    def from_random(cls, n_nodes: int, n_edges: int, dim: int = 4, seed: Optional[int] = None) -> SimpleVoid:
        """生成随机 Void 网络"""
        if seed is not None:
            random.seed(seed)
        void = cls(nodes=list(range(n_nodes)), _dim=dim)
        for _ in range(n_edges):
            u, v = random.sample(range(n_nodes), 2)
            void.add_edge(u, v, weight=random.uniform(0.5, 2.0))
        return void

    @classmethod
    def from_grid(cls, size: int, dim: int = 2) -> SimpleVoid:
        """生成规则网格 Void 网络"""
        void = cls(_dim=dim)
        for i in range(size ** dim):
            void.nodes.append(i)
        # 简化：只添加相邻节点连接
        for i in range(size ** dim):
            for j in range(i + 1, size ** dim):
                if random.random() < 0.1:
                    void.add_edge(i, j)
        return void


@dataclass
class SimpleMass(Mass):
    """
    简单 Mass 实现：标量物理量。
    """

    _value: float = 0.0
    _uncertainty: float = 0.0
    _confidence: float = 0.0
    _label: str = ""
    _metadata: Dict[str, Any] = field(default_factory=dict)

    def value(self) -> float:
        return self._value

    def uncertainty(self) -> float:
        return self._uncertainty

    def confidence(self) -> float:
        return self._confidence

    def __repr__(self) -> str:
        return f"SimpleMass({self._label} v={self._value:.6f}, σ={self._uncertainty:.6f}, c={self._confidence:.3f})"


class ConnectivityEmergenceRule(EmergenceRule):
    """
    连通性涌现规则：从 Void 网络的连通性涌现出物理量。

    参考：alpha_derivation/12_gravity_em_unification.md
    核心假设：电荷 e 是因果网络中节点"连通性"的涌现度量。
    """

    def __init__(self, target_label: str = "connectivity_mass", scale_factor: float = 1.0):
        self._name = target_label
        self._scale = scale_factor

    def apply(self, void: Void) -> Mass:
        topo = void.topology()
        n_nodes = topo.get("nodes", 0)
        n_edges = topo.get("edges", 0)
        avg_degree = topo.get("average_degree", 0.0)

        # 连通性涌现公式：mass ∝ sqrt(edges/nodes) * scale_factor
        if n_nodes > 0:
            raw_value = math.sqrt(n_edges / n_nodes) * avg_degree * self._scale
        else:
            raw_value = 0.0

        uncertainty = raw_value * 0.1  # 10% 启发式不确定性
        confidence = min(1.0, 0.5 + 0.1 * avg_degree)  # 连通性越高，置信度越高

        return SimpleMass(
            _value=raw_value,
            _uncertainty=uncertainty,
            _confidence=confidence,
            _label=self._name,
            _metadata={
                "nodes": n_nodes,
                "edges": n_edges,
                "avg_degree": avg_degree,
                "dimension": void.dimension(),
            }
        )

    def name(self) -> str:
        return "ConnectivityEmergence"

    def description(self) -> str:
        return "mass = sqrt(edges/nodes) * avg_degree * scale_factor"


class StabilityConvergenceCriterion(ConvergenceCriterion):
    """
    稳定性收敛准则：要求历史结果的标准差小于阈值。
    """

    def __init__(self, threshold: float = 0.05, min_history: int = 3):
        self._threshold = threshold
        self._min_history = min_history

    def evaluate(self, mass: Mass, history: List[Mass]) -> bool:
        if len(history) < self._min_history:
            return False
        values = [m.value() for m in history[-self._min_history:]]
        if not values:
            return False
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std_dev = math.sqrt(variance)
        relative_std = std_dev / abs(mean) if mean != 0 else (0.0 if std_dev == 0 else float("inf"))
        return relative_std < self._threshold and mass.confidence() > 0.5

    def name(self) -> str:
        return f"Stability(threshold={self._threshold})"


# ============================================================
# SECTION 5: ZhiKong Engine — 主控制引擎
# ============================================================

class ZhiKongEngine:
    """
    质空论涌现引擎 (ZhiKong Emergence Engine) — PFE Phase 4 核心组件。

    工作流：
        1. 接收 Void 输入（抽象拓扑网络）
        2. 应用 EmergenceRule 生成候选 Mass
        3. 只有提供 state_update 时才执行状态迭代和收敛判定
        4. 无状态更新时仅做单次评估，返回 converged=False

    数值稳定或启发式收敛不是物理真实性的证据。
    """

    def __init__(
        self,
        rule: Optional[EmergenceRule] = None,
        criterion: Optional[ConvergenceCriterion] = None,
        max_iterations: int = 100,
        verbose: bool = False,
        state_update: Optional[Callable[[Void, Mass, int], Void]] = None,
    ):
        if max_iterations < 1:
            raise ValueError("max_iterations must be at least 1")
        self.rule = rule or ConnectivityEmergenceRule()
        self.criterion = criterion or StabilityConvergenceCriterion()
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.state_update = state_update
        self._history: List[Mass] = []
        self._iteration_count = 0

    def run(self, void: Void) -> Tuple[Mass, bool]:
        """Return ``(mass, converged)``; a static evaluation is not convergence."""
        self._history = []
        self._iteration_count = 0

        if self.state_update is None:
            self._iteration_count = 1
            mass = self.rule.apply(void)
            self._history.append(mass)
            if self.verbose:
                print("[ZhiKong] Static single-pass evaluation; no iterative convergence claimed")
            return mass, False

        current_void = void
        for i in range(self.max_iterations):
            self._iteration_count = i + 1
            mass = self.rule.apply(current_void)
            self._history.append(mass)
            converged = self.criterion.evaluate(mass, self._history)

            if self.verbose:
                print(f"[ZhiKong] Iteration {i+1}: {mass}, converged={converged}")
            if converged:
                return mass, True
            current_void = self.state_update(current_void, mass, i)

        return self._history[-1], False

    def run_batch(self, voids: List[Void]) -> List[Tuple[Mass, bool]]:
        """批量运行涌现引擎"""
        return [self.run(v) for v in voids]

    def history(self) -> List[Mass]:
        return self._history.copy()

    def __repr__(self) -> str:
        return f"ZhiKongEngine(rule={self.rule.name()}, criterion={self.criterion.name()})"


# ============================================================
# SECTION 6: UTILITY FUNCTIONS
# ============================================================

def emerge(void: Void, rule: Optional[EmergenceRule] = None) -> Mass:
    """便捷函数：单次涌现"""
    engine = ZhiKongEngine(rule=rule, max_iterations=1)
    mass, _ = engine.run(void)
    return mass


def demo():
    """质空论涌现引擎演示"""
    print("=" * 60)
    print("ZhiKong Mass-Void Theory — Emergence Engine Demo")
    print("=" * 60)

    # 创建 Void 网络
    void = SimpleVoid.from_random(n_nodes=100, n_edges=200, dim=4, seed=42)
    print(f"\n[Void] Created: {void}")
    print(f"[Void] Topology: {void.topology()}")

    # 创建涌现引擎
    engine = ZhiKongEngine(
        rule=ConnectivityEmergenceRule(scale_factor=1.0),
        criterion=StabilityConvergenceCriterion(threshold=0.01, min_history=5),
        max_iterations=20,
        verbose=True,
    )

    print(f"\n[Engine] {engine}")
    print("\nRunning emergence...")

    mass, converged = engine.run(void)

    print(f"\n[Result] Iterative converged={converged} (no state_update: static single-pass only)")
    print(f"[Result] Heuristic mass={mass}; this is not physical confirmation")

    return mass, converged


if __name__ == "__main__":
    demo()
