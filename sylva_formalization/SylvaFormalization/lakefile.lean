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
    `BSD,
    `Complexity,
    `CookLevin,
    `CP004,
    `CP004_B2,
    `DynamicalSystem,
    `EllipticCurveReduction,
    `EmergentMath,
    `EntropyGapSpectral,
    `FourForcesUnification,
    `GravitationalField,
    `Hodge,
    `LocalGlobal,
    `MathAgent,
    `NavierStokes,
    `NumericalZeros,
    `QFT,
    `QuantumArithmetic,
    `RadiationTracker,
    `RiemannHypothesis,
    `SAIPTest,
    `StatisticalMechanics,
    `Superconductivity_Pairing_Framework,
    `SylvaInfrastructure,
    `TestMul,
    `TestNP,
    `TestSInf,
    `TestSuite,
    `ZetaVerifier
  ]
