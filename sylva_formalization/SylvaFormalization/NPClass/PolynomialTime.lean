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
theorem add {f g : ℕ → ℕ} (hf : IsPolynomial f) (hg : IsPolynomial g) :
    IsPolynomial (fun n => f n + g n) := by
  rcases hf with ⟨c₁, d₁, h₁⟩
  rcases hg with ⟨c₂, d₂, h₂⟩
  use c₁ + c₂, max d₁ d₂
  intro n
  have h1' := h₁ n
  have h2' := h₂ n
  have h3 : c₁ * n ^ d₁ + c₁ ≤ (c₁ + c₂) * n ^ max d₁ d₂ + (c₁ + c₂) := by
    have h4 : n ^ d₁ ≤ n ^ max d₁ d₂ := by
      apply Nat.pow_le_pow_of_le_right
      · by_cases hn : n = 0
        · subst hn; simp
        · exact Nat.zero_lt_of_ne_zero hn
      · exact Nat.le_max_left d₁ d₂
    nlinarith [h4]
  have h4 : c₂ * n ^ d₂ + c₂ ≤ (c₁ + c₂) * n ^ max d₁ d₂ + (c₁ + c₂) := by
    have h5 : n ^ d₂ ≤ n ^ max d₁ d₂ := by
      apply Nat.pow_le_pow_of_le_right
      · by_cases hn : n = 0
        · subst hn; simp
        · exact Nat.zero_lt_of_ne_zero hn
      · exact Nat.le_max_right d₁ d₂
    nlinarith [h5]
  linarith [h1', h2', h3, h4]

/-- Polynomials are closed under multiplication. -/
theorem mul {f g : ℕ → ℕ} (hf : IsPolynomial f) (hg : IsPolynomial g) :
    IsPolynomial (fun n => f n * g n) := by
  rcases hf with ⟨c₁, d₁, h₁⟩
  rcases hg with ⟨c₂, d₂, h₂⟩
  use (c₁ + 1) * (c₂ + 1), d₁ + d₂
  intro n
  have h1' := h₁ n
  have h2' := h₂ n
  have h3 : f n ≤ (c₁ + 1) * n ^ d₁ := by nlinarith
  have h4 : g n ≤ (c₂ + 1) * n ^ d₂ := by nlinarith
  have h5 : f n * g n ≤ (c₁ + 1) * n ^ d₁ * ((c₂ + 1) * n ^ d₂) := by
    apply Nat.mul_le_mul h3 h4
  have h6 : (c₁ + 1) * n ^ d₁ * ((c₂ + 1) * n ^ d₂) = (c₁ + 1) * (c₂ + 1) * n ^ (d₁ + d₂) := by
    rw [Nat.pow_add]
    ring
  have h7 : f n * g n ≤ (c₁ + 1) * (c₂ + 1) * n ^ (d₁ + d₂) := by
    linarith [h5, h6]
  have h8 : (c₁ + 1) * (c₂ + 1) * n ^ (d₁ + d₂) ≤ (c₁ + 1) * (c₂ + 1) * n ^ (d₁ + d₂) + (c₁ + 1) * (c₂ + 1) := by
    omega
  linarith [h7, h8]

/-- Polynomials are closed under composition. -/
theorem comp {f g : ℕ → ℕ} (hf : IsPolynomial f) (hg : IsPolynomial g) :
    IsPolynomial (fun n => f (g n)) := by
  rcases hf with ⟨c₁, d₁, h₁⟩
  rcases hg with ⟨c₂, d₂, h₂⟩
  use c₁ + c₂, d₁ * d₂
  intro n
  have h1' := h₁ (g n)
  have h2' := h₂ n
  have h3 : g n ≤ c₂ * n ^ d₂ + c₂ := h2'
  have h4 : f (g n) ≤ c₁ * (g n) ^ d₁ + c₁ := h1'
  have h5 : (g n) ^ d₁ ≤ (c₂ * n ^ d₂ + c₂) ^ d₁ := by
    apply Nat.pow_le_pow_of_le_left
    exact h3
  have h6 : c₁ * (g n) ^ d₁ + c₁ ≤ c₁ * (c₂ * n ^ d₂ + c₂) ^ d₁ + c₁ := by
    nlinarith [h5]
  have h7 : c₁ * (c₂ * n ^ d₂ + c₂) ^ d₁ + c₁ ≤ (c₁ + c₂) * n ^ (d₁ * d₂) + (c₁ + c₂) := by
    -- This is a coarse bound but sufficient for the definition
    have h8 : (c₂ * n ^ d₂ + c₂) ^ d₁ ≤ (c₂ + 1) ^ d₁ * (n ^ d₂ + 1) ^ d₁ := by
      have h9 : c₂ * n ^ d₂ + c₂ ≤ (c₂ + 1) * (n ^ d₂ + 1) := by
        nlinarith
      apply Nat.pow_le_pow_of_le_left
      exact h9
    have h10 : (n ^ d₂ + 1) ^ d₁ ≤ 2 ^ d₁ * n ^ (d₁ * d₂) := by
      have h11 : n ^ d₂ + 1 ≤ 2 * n ^ d₂ := by
        cases n with
        | zero => simp
        | succ n =>
          have h12 : (n + 1 : ℕ) ^ d₂ ≥ 1 := by
            apply Nat.one_le_pow
            exact Nat.succ_le_succ (Nat.zero_le n)
          nlinarith
      have h13 : (n ^ d₂ + 1) ^ d₁ ≤ (2 * n ^ d₂) ^ d₁ := by
        apply Nat.pow_le_pow_of_le_left
        exact h11
      rw [Nat.mul_pow] at h13
      have h14 : (2 * n ^ d₂) ^ d₁ = 2 ^ d₁ * (n ^ d₂) ^ d₁ := by
        rw [Nat.mul_pow]
      have h15 : (n ^ d₂) ^ d₁ = n ^ (d₂ * d₁) := by
        rw [← Nat.pow_mul]
      have h16 : n ^ (d₂ * d₁) = n ^ (d₁ * d₂) := by
        rw [Nat.mul_comm]
      nlinarith [h13, h14, h15, h16]
    nlinarith [h8, h10]
  linarith [h4, h6, h7]

/-- Monotonicity: if f ≤ g and g is polynomial, then f is polynomial. -/
theorem mono {f g : ℕ → ℕ} (hle : ∀ n, f n ≤ g n) (hg : IsPolynomial g) :
    IsPolynomial f := by
  rcases hg with ⟨c, d, h⟩
  use c, d
  intro n
  linarith [hle n, h n]

end IsPolynomial

end Sylva.NPClass
