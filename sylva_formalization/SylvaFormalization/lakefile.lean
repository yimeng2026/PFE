import Lake
open Lake DSL

package «SylvaFormalization» where
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩,
    ⟨`pp.proofs.withType, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "8a178386ffc0f5fef0b77738bb5449d50efeea95"

@[default_target]
lean_lib «SylvaFormalization» where
  roots := #[
    `BCSTherory,
    `BerryConnection,
    `BerryCurvature,
    `BlochTheorem,
    `ChernNumber,
    `ChernSimons,
    `CondensedMatter.Superconductivity,
    `ContinuumLimit,
    `CookLevin.SAT,
    `Cosmology.DarkEnergy,
    `Cosmology.Inflation,
    `DeterminantComplexity,
    `EinsteinCartan,
    `FifteenConstants,
    `GraphTheoreticCharge,
    `Hodge,
    `InformationGeometry,
    `NPClass.PolynomialTime,
    `Renormalization,
    `RiemannHypothesis,
    `SAT,
    `StandardModel.Basic,
    `StringTheory.Basic,
    `SylvaInfrastructure,
    `TopologicalInsulator,
    `NavierStokes,
    `ZetaVerifier_backup
  ]
