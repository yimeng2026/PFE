"""Regression tests for PFE topology metrics and convergence semantics."""

from dataclasses import dataclass
from typing import Any, Dict, Union

import pytest

from pfe_emergence.mass_void_theory import (
    EmergenceRule,
    Mass,
    SimpleMass,
    SimpleVoid,
    StabilityConvergenceCriterion,
    Void,
    ZhiKongEngine,
)


def test_weighted_connectivity_counts_each_incident_edge_once():
    void = SimpleVoid(nodes=[0, 1, 2, 3])
    void.add_edge(0, 1, weight=2.5)
    void.add_edge(1, 2, weight=1.5)
    void.edges.append((2, 0))  # An explicitly supplied unweighted edge defaults to 1.

    assert void.connectivity(0) == pytest.approx(3.5)
    assert void.connectivity("1") == pytest.approx(4.0)
    assert void.connectivity(2) == pytest.approx(2.5)
    assert void.connectivity(3) == 0.0
    assert void.connectivity(99) == 0.0


def test_static_void_is_single_pass_not_iterative_convergence():
    void = SimpleVoid(nodes=[0, 1])
    void.add_edge(0, 1)
    engine = ZhiKongEngine(
        criterion=StabilityConvergenceCriterion(threshold=1.0, min_history=1),
        max_iterations=20,
    )

    mass, converged = engine.run(void)

    assert mass.value() > 0
    assert converged is False
    assert len(engine.history()) == 1
    assert engine._iteration_count == 1


@dataclass
class ScalarVoid(Void):
    scalar: float

    def topology(self) -> Dict[str, Any]:
        return {"nodes": 1, "edges": 0, "average_degree": 0.0}

    def dimension(self) -> int:
        return 1

    def connectivity(self, node_id: Union[int, str]) -> float:
        return 0.0


class ScalarRule(EmergenceRule):
    def apply(self, void: Void) -> Mass:
        assert isinstance(void, ScalarVoid)
        return SimpleMass(_value=void.scalar, _confidence=1.0, _label="test scalar")

    def name(self) -> str:
        return "ScalarRule"

    def description(self) -> str:
        return "Expose the current test state as a scalar"


def test_state_update_is_required_and_supports_actual_iteration():
    void = ScalarVoid(3.0)

    def settle_to_one(current: Void, mass: Mass, iteration: int) -> Void:
        assert isinstance(current, ScalarVoid)
        current.scalar = 1.0
        return current

    engine = ZhiKongEngine(
        rule=ScalarRule(),
        criterion=StabilityConvergenceCriterion(threshold=0.01, min_history=3),
        max_iterations=10,
        state_update=settle_to_one,
    )
    mass, converged = engine.run(void)

    assert converged is True
    assert mass.value() == 1.0
    assert [item.value() for item in engine.history()] == [3.0, 1.0, 1.0, 1.0]


def test_zero_history_can_be_stable_and_invalid_iteration_count_fails():
    zero = SimpleMass(_value=0.0, _confidence=1.0)
    criterion = StabilityConvergenceCriterion(min_history=3)
    assert criterion.evaluate(zero, [zero, zero, zero]) is True
    with pytest.raises(ValueError):
        ZhiKongEngine(max_iterations=0)
