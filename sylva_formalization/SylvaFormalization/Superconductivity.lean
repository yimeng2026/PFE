/-
Superconductivity — Main entry point
=====================================

Pairing frameworks, material derivation, and BCS theory formalizations.

This file re-exports all submodules for backward compatibility.
New code should import specific submodules directly.

Submodules:
- Superconductivity.Superconductivity_Pairing_Framework   — Pairing mechanisms and gap equations
- Superconductivity.Superconductivity_Material_Derivation — Material-specific derivations
- Superconductivity.RadiationTracker                      — Proof radiation tracking (meta)
-/

import Superconductivity.Superconductivity_Pairing_Framework
import Superconductivity.Superconductivity_Material_Derivation
import Superconductivity.RadiationTracker
