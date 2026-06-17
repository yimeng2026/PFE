import Lake
open Lake DSL

package SylvaFormalization where
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩,
    ⟨`pp.proofs.withType, false⟩
  ]

require mathlib from "lake/packages/mathlib"

@[default_target]
lean_lib SylvaFormalization where
  roots := #[
    `Basic,
    `BCSTherory,
    `ChernNumber,
    `CondensedMatter,
    `CookLevin,
    `Cosmology,
    `EllipticCurveReduction,
    `FifteenConstants,
    `FourForcesUnification,
    `GaugeTheory,
    `Hodge,
    `InformationGeometry,
    `NPClass,
    `QuantumGravity,
    `Renormalization,
    `RiemannHypothesis,
    `SAT,
    `StandardModel,
    `StratifiedGeometry,
    `StringTheory,
    `SylvaInfrastructure,
    `TestSInf,
    `TopologicalInsulator
  ]
