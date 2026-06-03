/-
Sylva Formalization Project - Entry Point (FIXED)
==================================================

This entry point now includes all repaired modules:
- ZetaVerifier (FIXED - all proofs completed)
- RiemannHypothesis (FIXED - structure restored, numerics verified)

Modules still removed (pending repair):
- NumericalZeros  (corrupted, noncomputable issues)
- Hodge           (typeclass synthesis failures)

Modules RETAINED:
- Basic (foundation)
- Complexity
- BSD
- NavierStokes
- CP004
- CookLevin
- SylvaInfrastructure
- MathAgent
- ZetaVerifier (restored)
- RiemannHypothesis (restored)
-/

-- Level 0: Foundation Layer
import SylvaFormalization.Basic

-- Level 1: Core Modules
-- import SylvaFormalization.NumericalZeros  -- REMOVED (repair pending)
import SylvaFormalization.Complexity
import SylvaFormalization.BSD
import SylvaFormalization.EllipticCurveReduction
-- import SylvaFormalization.Hodge          -- REMOVED (repair pending)
import SylvaFormalization.NavierStokes
import SylvaFormalization.CP004

-- Level 2: Intermediate Modules
import SylvaFormalization.ZetaVerifier
import SylvaFormalization.RiemannHypothesis
import SylvaFormalization.CookLevin
import SylvaFormalization.SylvaInfrastructure

-- Level 3: Application Modules
import SylvaFormalization.MathAgent

namespace Sylva
end Sylva
