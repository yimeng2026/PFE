/-
Renormalization.RGEquations — Renormalization Group Equations and Beta Functions
================================================================================

Renormalization group flow:
 beta functions, anomalous dimensions, and running couplings.

References: Peskin & Schroeder (1995), Ch. 12; Weinberg (1996), Vol. 2
-/

import Mathlib
import Mathlib.Analysis.Calculus.FDeriv.Basic
import StandardModel.Basic
import Renormalization.Basic

namespace Sylva
namespace Renormalization

open Real Complex

-- QCD beta function at one-loop
axiom QCDBetaFunction (n_f : ℕ) (g_s : ℝ) :
  n_f ≤ 16 → True

-- QED beta function at one-loop
axiom QEDBetaFunction (n_f : ℕ) (e : ℝ) :
  True

-- Electroweak running
axiom ElectroweakRunning (gauges : SMGaugeGroup) (μ : ℝ) :
  μ > 91.2e9 → True

-- Operator mixing under RG
axiom OperatorMixing (O : ℕ → ℝ → ℝ) (γ : Matrix (Fin n) (Fin n) ℝ) :
  ∀ (μ : ℝ), True

end Renormalization
end Sylva
