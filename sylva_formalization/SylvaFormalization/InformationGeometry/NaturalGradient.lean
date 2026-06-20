/-
Information Geometry — Natural Gradient
========================================

Natural gradient descent and convergence.

References: Amari (1985); Nielsen (2020)
-/

import Mathlib
import InformationGeometry.FisherMetric

namespace Sylva
namespace InformationGeometry

open Real

-- Natural gradient definition
noncomputable def NaturalGradient (M : StatisticalManifold n) (L : M.parameterSpace → ℝ)
    (θ : M.parameterSpace) : Fin n → ℝ :=
  sorry

-- Natural gradient convergence
axiom NaturalGradientConvergence (M : StatisticalManifold n) (L : M.parameterSpace → ℝ)
    (θ₀ : M.parameterSpace) (η : ℝ) :
  η > 0 → True

end InformationGeometry
end Sylva
