"""
PFE Phase 4: ZhiKong Emergence Engine (质空论涌现引擎)

质空论 (ZhiKong = Mass-Void Theory) 核心哲学：
- 质 (Mass): 可测量、可验证的物理量与工程输出
- 空 (Void): 抽象拓扑网络、因果结构、数学框架
- 涌现 (Emergence): 从 Void 拓扑网络生成 Mass 物理量的自动化过程

PFE 不追求每一步的数学严格性，而是追求"有效涌现"——
通过工程手段（数值计算、LLM 推理、自动化代理）让"空"涌现出"质"。
"""

from .mass_void_theory import Mass, Void, EmergenceRule, ConvergenceCriterion, ZhiKongEngine
from .phi_engine import PhiEngine, SelfSimilarEmergence
from .level_ontology import LevelOntology, EmergenceLevel, LevelCoupling
from .causal_network_engine import CausalNode, CausalEdge, CausalNetwork, EmergenceMetric

__version__ = "4.0.0"
__all__ = [
    "Mass", "Void", "EmergenceRule", "ConvergenceCriterion", "ZhiKongEngine",
    "PhiEngine", "SelfSimilarEmergence",
    "LevelOntology", "EmergenceLevel", "LevelCoupling",
    "CausalNode", "CausalEdge", "CausalNetwork", "EmergenceMetric",
]
