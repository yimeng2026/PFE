#!/usr/bin/env python3
"""Check internal consistency of stored causal-network simulation results.

This validates JSON arithmetic and documentation inputs, not the physical model.
A deliberately corrupted in-memory copy is used as a negative control.
"""

import copy
import json
import math
import statistics
from pathlib import Path
from typing import Dict, List

DATA_PATH = Path(__file__).with_name("simulation_results.json")
EXPECTED_DIMENSIONS = {"2", "3", "4"}
EXPECTED_SIZES = {"1000", "5000", "10000"}


def validate_document(document: Dict) -> List[str]:
    errors: List[str] = []
    results = document.get("main_results", {})
    if set(results) != EXPECTED_DIMENSIONS:
        errors.append(
            f"dimension keys: expected {EXPECTED_DIMENSIONS}, got {set(results)}"
        )
    target = document.get("target_alpha")
    if not isinstance(target, (int, float)) or not math.isfinite(target) or target <= 0:
        errors.append("target_alpha must be a finite positive number")
        target = None
    elif not math.isclose(target, 1 / 137.036, rel_tol=0, abs_tol=1e-12):
        errors.append(
            f"target_alpha={target} is inconsistent with the declared 1/137.036"
        )

    for dimension in EXPECTED_DIMENSIONS & set(results):
        by_size = results[dimension]
        if set(by_size) != EXPECTED_SIZES:
            errors.append(
                f"d={dimension} sizes: expected {EXPECTED_SIZES}, got {set(by_size)}"
            )
        for size in EXPECTED_SIZES & set(by_size):
            record = by_size[size]
            samples = record.get("all_alphas", [])
            label = f"d={dimension}, N={size}"
            if len(samples) != 5 or not all(
                isinstance(value, (int, float)) and math.isfinite(value) and value > 0
                for value in samples
            ):
                errors.append(f"{label}: expected five finite positive alpha samples")
                continue
            mean = statistics.fmean(samples)
            std = statistics.pstdev(samples)
            if not math.isclose(record["alpha_mean"], mean, rel_tol=0, abs_tol=1e-12):
                errors.append(
                    f"{label}: alpha_mean={record['alpha_mean']}, recomputed={mean}"
                )
            if not math.isclose(record["alpha_std"], std, rel_tol=0, abs_tol=1e-12):
                errors.append(
                    f"{label}: alpha_std={record['alpha_std']}, recomputed={std}"
                )
            expected_degree = record["density"] * (int(size) - 1)
            if not math.isclose(
                record["mean_degree"], expected_degree, rel_tol=0, abs_tol=1e-8
            ):
                errors.append(
                    f"{label}: mean_degree={record['mean_degree']}, "
                    f"density*(N-1)={expected_degree}"
                )
    return errors


def run_all_tests() -> int:
    document = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    errors = validate_document(document)
    for error in errors:
        print(f"[FAIL] {error}")
    if not errors:
        print(
            "[PASS] Stored sample means, population standard deviations and densities agree"
        )

    corrupted = copy.deepcopy(document)
    corrupted["main_results"]["4"]["10000"]["alpha_mean"] += 1.0
    negative_errors = validate_document(corrupted)
    if negative_errors:
        print("[PASS] Negative control rejected a corrupted alpha_mean")
    else:
        errors.append("negative control was not detected")
        print("[FAIL] Negative control was not detected")

    target = document["target_alpha"]
    print("Stored values (descriptive only; not physical confirmation):")
    for dimension in sorted(EXPECTED_DIMENSIONS):
        for size in sorted(EXPECTED_SIZES, key=int):
            alpha = document["main_results"][dimension][size]["alpha_mean"]
            deviation = (alpha / target - 1) * 100
            print(
                f"  d={dimension}, N={size}: alpha={alpha:.10f}, delta={deviation:+.3f}%"
            )

    print(f"Consistency summary: {'FAIL' if errors else 'PASS'}; errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(run_all_tests())
