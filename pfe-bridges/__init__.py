#!/usr/bin/env python3
"""
pfe-bridges — PFE ↔ TOE-SYLVA 桥接模块

工程应用分支 (PFE) 与形式化学术分支 (TOE-SYLVA) 之间的桥接层。
通过千界花园 (Blooming Garden) 作为中介，实现：
- 数值验证 ↔ 形式化定理的映射
- LLM 工程策略 ↔ 学术证明启发
- 多代理并行验证

模块:
- base_bridge: 抽象基类 PFEProblemBridge
- qianjie_bridge: 千界花园 API 客户端与集成桥接
- agent_coordinator: 多代理调度与结果聚合

PFE ENGINEERING NOTE: 不追求数学严格，追求有效涌现。
"""

__version__ = "0.1.0"
__all__ = [
    "PFEProblemBridge",
    "BridgeStatus",
    "ConfidenceLevel",
    "NumericalVerificationResult",
    "HeuristicStrategy",
    "BridgeRunResult",
    "QianJieClient",
    "QianJieConfig",
    "QianJieBridge",
    "SylvaSyncStatus",
    "LLMStrategyRequest",
    "PFEAgentCoordinator",
    "PFEEngineeringMode",
    "CoordinatorConfig",
    "CoordinatorReport",
    "AgentTask",
]

from .base_bridge import (
    PFEProblemBridge,
    BridgeStatus,
    ConfidenceLevel,
    NumericalVerificationResult,
    HeuristicStrategy,
    BridgeRunResult,
)

from .qianjie_bridge import (
    QianJieClient,
    QianJieConfig,
    QianJieBridge,
    SylvaSyncStatus,
    LLMStrategyRequest,
)

from .agent_coordinator import (
    PFEAgentCoordinator,
    PFEEngineeringMode,
    CoordinatorConfig,
    CoordinatorReport,
    AgentTask,
)
