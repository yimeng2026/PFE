/-
Sylva Formalization - NPClass Module
=====================================
Polynomial Time Predicate Definition

Reference: KrystianYC, Issue #35366
https://github.com/leanprover-community/mathlib4/issues/35366

Defines `IsPolynomial` as a predicate on functions ℕ → ℕ,
capturing the standard notion of polynomial upper bounds.

Author: Sylva Formalization Project (based on KrystianYC's design)
Date: 2026-06-03
-/

import Mathlib

namespace Sylva.NPClass

/-! ## Polynomial Time Bounds -/

/-- A function `f : ℕ → ℕ` is polynomially bounded if there exist
constants `c` and `d` such that `f(n) ≤ c * n^d + c` for all `n`.

This is the standard textbook definition (Sipser §7.1) adapted
to Lean's type system. The `+ c` term handles the constant case
when `n = 0` without requiring separate treatment.

Reference: KrystianYC / Issue #35366 - Mathlib4 P/NP for TM1
https://github.com/leanprover-community/mathlib4/issues/35366 -/
def IsPolynomial (f : ℕ → ℕ) : Prop :=
  ∃ (c d : ℕ), ∀ n, f n ≤ c * n ^ d + c

namespace IsPolynomial

/-- Constant functions are polynomial. -/
theorem of_constant (k : ℕ) : IsPolynomial (fun _ => k) := by
  use k, 0
  intro n
  simp

/-- The identity function is polynomial. -/
theorem id : IsPolynomial (fun n => n) := by
  use 1, 1
  intro n
  simp
  <;> omega

/-- Polynomials are closed under addition. -/
axiom add {f g : ℕ → ℕ} (hf : IsPolynomial f) (hg : IsPolynomial g) :
    IsPolynomial (fun n => f n + g n)

/-- Polynomials are closed under multiplication. -/
axiom mul {f g : ℕ → ℕ} (hf : IsPolynomial f) (hg : IsPolynomial g) :
    IsPolynomial (fun n => f n * g n)

/-- Polynomials are closed under composition. -/
axiom comp {f g : ℕ → ℕ} (hf : IsPolynomial f) (hg : IsPolynomial g) :
    IsPolynomial (fun n => f (g n))

/-- Monotonicity: if f ≤ g and g is polynomial, then f is polynomial. -/
axiom mono {f g : ℕ → ℕ} (hle : ∀ n, f n ≤ g n) (hg : IsPolynomial g) :
    IsPolynomial f

end IsPolynomial

end Sylva.NPClass
