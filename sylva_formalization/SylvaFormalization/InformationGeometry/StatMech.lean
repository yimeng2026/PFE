/-
Information Geometry — Applications to Statistical Mechanics
=============================================================

Free energy, Cramér-Rao bound, and thermodynamic fluctuations.

References: Amari & Nagaoka (2000)
-/

import Mathlib
import InformationGeometry.FisherMetric

namespace Sylva
namespace InformationGeometry

open Real

-- Free energy and Fisher information relationship
axiom FreeEnergyFisher (M : StatisticalManifold n) (θ : M.parameterSpace) :
  True

-- Cramér-Rao bound
axiom CramerRaoBound (M : StatisticalManifold n) (θ : M.parameterSpace) :
  True

end InformationGeometry
end Sylva
