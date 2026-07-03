"""
Causal Network Emergence Engine
因果网络涌现引擎

参考：alpha_derivation/12_gravity_em_unification.md 中的网络定义

核心定义：
- CausalNode: 因果网络节点（代表时空中的一个事件）
- CausalEdge: 因果边（代表两个事件之间的因果联系）
- CausalNetwork: 完整的因果网络，嵌入到 d 维时空中
- EmergenceMetric: 从网络连通性涌现出的物理量度量

核心假设（来自 alpha_derivation）：
物理真空的因果网络 C = (V, E, w) 具有内在的几何结构。
当网络嵌入到时空流形 M 时，连通性度量 C(v) 可以分解为：
- C_temporal(v): 时间方向的因果连通性 → 涌现为质量
- C_spatial(v): 空间截面上的手性连通性 → 涌现为电荷
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from .mass_void_theory import Mass, SimpleMass, Void
from .phi_engine import PHI


# ============================================================
# SECTION 1: CAUSAL NODE
# ============================================================

@dataclass
class CausalNode:
    """
    因果网络节点：代表时空中的一个事件。

    参考：alpha_derivation/01_causal_network_simulation.py
    """

    id: int
    position: np.ndarray  # d维时空坐标 (t, x, y, z, ...)
    degree: int = 0
    past_neighbors: List[int] = field(default_factory=list)
    future_neighbors: List[int] = field(default_factory=list)
    temporal_connectivity: float = 0.0
    spatial_connectivity: float = 0.0

    def __post_init__(self):
        if not isinstance(self.position, np.ndarray):
            self.position = np.array(self.position)

    def time(self) -> float:
        """返回时间坐标（第0维）"""
        return float(self.position[0]) if len(self.position) > 0 else 0.0

    def spatial(self) -> np.ndarray:
        """返回空间坐标（第1维及以后）"""
        return self.position[1:] if len(self.position) > 1 else np.array([])

    def __repr__(self) -> str:
        return f"CausalNode(id={self.id}, t={self.time():.4f}, deg={self.degree})"


# ============================================================
# SECTION 2: CAUSAL EDGE
# ============================================================

@dataclass
class CausalEdge:
    """
    因果边：代表两个事件之间的因果联系。

    边的权重 w(u,v) 表示因果联系的强度。
    """

    source: int
    target: int
    weight: float = 1.0
    temporal_separation: float = 0.0
    spatial_separation: float = 0.0
    is_timelike: bool = True  # 类时间隔（因果相关）或类空间隔（因果无关）

    def __repr__(self) -> str:
        return f"CausalEdge({self.source}→{self.target}, w={self.weight:.4f})"


# ============================================================
# SECTION 3: CAUSAL NETWORK
# ============================================================

class CausalNetwork(Void):
    """
    d维因果网络模型。

    节点代表事件，边代表因果联系（类时间隔）。
    核心假设：电荷 e 是因果网络中节点"连通性"的涌现度量。

    参考：alpha_derivation/01_causal_network_simulation.py 中的 CausalNetwork
    """

    def __init__(
        self,
        dim: int = 4,
        num_nodes: int = 100,
        time_extent: float = 1.0,
        space_extent: float = 1.0,
        speed_of_light: float = 1.0,
    ):
        self.dim = dim
        self.num_nodes = num_nodes
        self.time_extent = time_extent
        self.space_extent = space_extent
        self.speed_of_light = speed_of_light
        self.nodes: List[CausalNode] = []
        self.edges: List[CausalEdge] = []
        self.adjacency: Dict[Tuple[int, int], CausalEdge] = {}

    def generate_nodes(self, seed: Optional[int] = None) -> None:
        """在 d 维时空中均匀随机分布节点"""
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        for i in range(self.num_nodes):
            t = random.uniform(0, self.time_extent)
            spatial_coords = np.random.uniform(
                -self.space_extent / 2,
                self.space_extent / 2,
                self.dim - 1,
            )
            position = np.concatenate([[t], spatial_coords])
            self.nodes.append(CausalNode(id=i, position=position))

    def build_causal_edges(self) -> None:
        """
        构建因果边。

        因果条件：两个节点之间如果满足类时间隔，则存在因果边。
        即：Δt > |Δx| / c（光锥条件）
        """
        self.edges = []
        self.adjacency = {}

        for i, node_i in enumerate(self.nodes):
            for j, node_j in enumerate(self.nodes):
                if i == j:
                    continue

                dt = node_j.time() - node_i.time()
                if dt <= 0:
                    continue  # 只考虑向前的因果联系

                dx = np.linalg.norm(node_j.spatial() - node_i.spatial())
                if dx > self.speed_of_light * dt:
                    continue  # 类空间隔，无因果联系

                # 类时间隔，建立因果边
                weight = 1.0 / (1.0 + dx / (self.speed_of_light * dt + 1e-10))
                edge = CausalEdge(
                    source=i,
                    target=j,
                    weight=weight,
                    temporal_separation=dt,
                    spatial_separation=dx,
                    is_timelike=True,
                )
                self.edges.append(edge)
                self.adjacency[(i, j)] = edge

                node_i.future_neighbors.append(j)
                node_j.past_neighbors.append(i)

        # 更新度数
        for node in self.nodes:
            node.degree = len(node.past_neighbors) + len(node.future_neighbors)

    def compute_connectivity(self) -> None:
        """
        计算每个节点的连通性度量。

        C_temporal(v): 时间方向的连通性（过去+未来邻居数）
        C_spatial(v): 空间方向的连通性（空间分离的倒数）
        """
        for node in self.nodes:
            # 时间连通性
            node.temporal_connectivity = len(node.past_neighbors) + len(node.future_neighbors)

            # 空间连通性（基于空间分离的加权平均）
            spatial_sum = 0.0
            for neighbor_id in node.past_neighbors + node.future_neighbors:
                edge = self.adjacency.get((node.id, neighbor_id)) or self.adjacency.get((neighbor_id, node.id))
                if edge:
                    spatial_sum += edge.weight / (edge.spatial_separation + 1e-10)
            node.spatial_connectivity = spatial_sum

    def degree_distribution(self) -> Dict[int, int]:
        """返回度分布"""
        dist = {}
        for node in self.nodes:
            d = node.degree
            dist[d] = dist.get(d, 0) + 1
        return dist

    def average_degree(self) -> float:
        """返回平均度数"""
        if not self.nodes:
            return 0.0
        return sum(node.degree for node in self.nodes) / len(self.nodes)

    def average_clustering(self) -> float:
        """返回平均聚类系数（简化计算）"""
        if not self.nodes:
            return 0.0

        clustering = []
        for node in self.nodes:
            neighbors = set(node.past_neighbors + node.future_neighbors)
            if len(neighbors) < 2:
                continue

            # 计算邻居之间的连接数
            links = 0
            for n1 in neighbors:
                for n2 in neighbors:
                    if n1 != n2 and ((n1, n2) in self.adjacency or (n2, n1) in self.adjacency):
                        links += 1
            possible = len(neighbors) * (len(neighbors) - 1)
            if possible > 0:
                clustering.append(links / possible)

        return sum(clustering) / len(clustering) if clustering else 0.0

    def topology(self) -> Dict[str, any]:
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "average_degree": self.average_degree(),
            "dimension": self.dim,
            "time_extent": self.time_extent,
            "space_extent": self.space_extent,
        }

    def dimension(self) -> int:
        return self.dim

    def connectivity(self, node_id: Union[int, str]) -> float:
        nid = int(node_id)
        if 0 <= nid < len(self.nodes):
            node = self.nodes[nid]
            return node.temporal_connectivity + node.spatial_connectivity
        return 0.0

    @classmethod
    def generate_random(
        cls,
        dim: int = 4,
        num_nodes: int = 100,
        seed: Optional[int] = None,
    ) -> CausalNetwork:
        """生成随机因果网络"""
        network = cls(dim=dim, num_nodes=num_nodes)
        network.generate_nodes(seed=seed)
        network.build_causal_edges()
        network.compute_connectivity()
        return network

    def __repr__(self) -> str:
        return f"CausalNetwork(dim={self.dim}, nodes={len(self.nodes)}, edges={len(self.edges)})"


# ============================================================
# SECTION 4: EMERGENCE METRICS
# ============================================================

class EmergenceMetric:
    """
    涌现度量：从因果网络连通性涌现出物理量。

    参考：alpha_derivation/12_gravity_em_unification.md

    核心假设：
    - 质量 m ∝ sqrt(C_temporal × K_loop)
    - 电荷 e ∝ C_spatial（手性连通性）
    - 精细结构常数 α = e² / 4π
    """

    def __init__(self, network: CausalNetwork):
        self.network = network

    def mass_emergence(self, node_id: int) -> float:
        """
        质量涌现：从时间连通性涌现。

        m ∝ sqrt(C_temporal × K_loop)
        """
        if 0 <= node_id < len(self.network.nodes):
            node = self.network.nodes[node_id]
            ct = node.temporal_connectivity
            # K_loop: 因果环路复杂度（用平均聚类系数近似）
            k_loop = self.network.average_clustering() + 1e-10
            return math.sqrt(ct * k_loop)
        return 0.0

    def charge_emergence(self, node_id: int) -> float:
        """
        电荷涌现：从空间连通性涌现。

        e ∝ C_spatial
        """
        if 0 <= node_id < len(self.network.nodes):
            node = self.network.nodes[node_id]
            return node.spatial_connectivity
        return 0.0

    def alpha_emergence(self) -> float:
        """
        精细结构常数涌现。

        α = <e>² / (4π) × coupling_factor
        """
        if not self.network.nodes:
            return 0.0

        avg_charge = sum(
            self.charge_emergence(i) for i in range(len(self.network.nodes))
        ) / len(self.network.nodes)

        if avg_charge <= 0:
            return 0.0

        return (avg_charge ** 2) / (4 * math.pi)

    def gravitational_coupling(self) -> float:
        """
        引力耦合涌现。

        G ∝ 1 / (network_connectivity)²
        """
        avg_conn = self.network.average_degree()
        if avg_conn <= 0:
            return 0.0
        return 1.0 / (avg_conn ** 2)

    def mass_to_charge_ratio(self, node_id: int) -> float:
        """质量-电荷比"""
        m = self.mass_emergence(node_id)
        e = self.charge_emergence(node_id)
        if e == 0:
            return float('inf')
        return m / e

    def emergence_summary(self, node_id: int) -> Dict[str, float]:
        """返回指定节点的涌现摘要"""
        return {
            "mass": self.mass_emergence(node_id),
            "charge": self.charge_emergence(node_id),
            "mass_charge_ratio": self.mass_to_charge_ratio(node_id),
            "alpha_global": self.alpha_emergence(),
            "gravitational_coupling": self.gravitational_coupling(),
            "temporal_connectivity": self.network.nodes[node_id].temporal_connectivity if node_id < len(self.network.nodes) else 0.0,
            "spatial_connectivity": self.network.nodes[node_id].spatial_connectivity if node_id < len(self.network.nodes) else 0.0,
        }

    def __repr__(self) -> str:
        return f"EmergenceMetric(network={self.network})"


# ============================================================
# SECTION 5: UTILITY FUNCTIONS
# ============================================================

def demo():
    """因果网络涌现引擎演示"""
    print("=" * 60)
    print("Causal Network Emergence Engine Demo")
    print("=" * 60)

    print(f"\n[Network Generation]")
    network = CausalNetwork.generate_random(dim=4, num_nodes=50, seed=42)
    print(f"  {network}")
    print(f"  Topology: {network.topology()}")

    print(f"\n[Degree Distribution]")
    dist = network.degree_distribution()
    for degree, count in sorted(dist.items())[:10]:
        print(f"  degree={degree}: {count} nodes")

    print(f"\n[Emergence Metrics]")
    metric = EmergenceMetric(network)

    for node_id in [0, 1, 2]:
        summary = metric.emergence_summary(node_id)
        print(f"  Node {node_id}:")
        for key, value in summary.items():
            print(f"    {key}: {value:.6f}")

    print(f"\n[Global Constants]")
    print(f"  Alpha (emergence): {metric.alpha_emergence():.6f}")
    print(f"  Gravitational coupling: {metric.gravitational_coupling():.6f}")

    return network, metric


if __name__ == "__main__":
    demo()
