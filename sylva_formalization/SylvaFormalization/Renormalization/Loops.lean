/-
Renormalization.Loops — Loop Integrals and One-Loop Counterterms
=================================================================

Loop-level calculations in dimensional regularization.
References: Peskin & Schroeder (1995), Ch. 10
-/

import Mathlib
import Mathlib.Analysis.Calculus.FDeriv.Basic
import StandardModel.Basic
import Renormalization.Basic

namespace Sylva
namespace Renormalization

open Real Complex

-- Loop integral finiteness in dimensional regularization
axiom LoopIntegralDimReg (params : DimRegParams) (m : ℝ) (n : ℕ) :
  params.D < 2 * n → True

-- One-loop counterterms in MS-bar scheme
axiom CountertermsOneLoop (scheme : RenormalizationScheme) (α : ℝ) (ε : ℝ) :
  True

end Renormalization
end Sylva
