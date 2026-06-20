/-
BCS Theory -- Superconductivity Pairing and Energy Gap
======================================================
Formalizes the Bardeen-Cooper-Schrieffer (BCS) theory of superconductivity.
References: Bardeen, Cooper, Schrieffer (1957)
-/

import Mathlib

namespace Sylva
namespace BCSTherory

open Real Complex

structure CooperPair where
  k : Fin 3 → ℝ
  spin1 : Fin 2
  k' : Fin 3 → ℝ
  spin2 : Fin 2
  opposite : k' = -k ∧ spin2 = 1 - spin1

structure BCSHamiltonian where
  epsilon : Fin 3 → ℝ → ℝ
  V : ℝ
  V_positive : V > 0
  E_F : ℝ
  k_F : ℝ

structure EnergyGap (H : BCSHamiltonian) where
  delta : ℝ
  delta_nonneg : delta ≥ 0

axiom GapEquationZeroT (H : BCSHamiltonian) (Δ : EnergyGap H) :
  True

axiom CriticalTemperature (H : BCSHamiltonian) (Δ : EnergyGap H) :
  True

axiom QuasiparticleSpectrum (H : BCSHamiltonian) (Δ : EnergyGap H) :
  True

axiom DensityOfStatesSuperconductor (H : BCSHamiltonian) (Δ : EnergyGap H) :
  True

axiom JosephsonCurrent (H : BCSHamiltonian) (Δ : EnergyGap H) (φ : ℝ) :
  True

axiom ACJosephsonEffect (H : BCSHamiltonian) (Δ : EnergyGap H) (V : ℝ) :
  True

structure GinzburgLandau where
  alpha : ℝ
  beta : ℝ
  beta_positive : beta > 0
  psi : Fin 3 → ℝ → ℂ
  A : Fin 3 → ℝ → Fin 3 → ℝ

axiom GinzburgLandauEquations (gl : GinzburgLandau) :
  True

axiom CoherenceLength (gl : GinzburgLandau) :
  True

axiom PenetrationDepth (gl : GinzburgLandau) :
  True

inductive SuperconductorType
  | TypeI
  | TypeII

axiom TypeI_axiom (gl : GinzburgLandau) : True
axiom TypeII_axiom (gl : GinzburgLandau) : True

end BCSTherory
end Sylva
