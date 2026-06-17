import Lake
open Lake DSL

package SylvaFormalization where
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩,
    ⟨`pp.proofs.withType, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.18.0"

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
    `StandardModel,
    `StringTheory,
    `SylvaInfrastructure,
    `TestSInf,
    `TopologicalInsulator
  ]
