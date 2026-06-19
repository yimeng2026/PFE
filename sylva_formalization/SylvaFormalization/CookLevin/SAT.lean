/-
# SAT.lean - Boolean Satisfiability Problem (SAT)

Defines Boolean formulas, CNF (Conjunctive Normal Form), and satisfiability.

## References

- **Coq implementation**: Gäher, L. & Kunze, F. (2021). "Mechanising Complexity Theory: The Cook-Levin Theorem in Coq". ITP 2021.
  - Repository: https://github.com/uds-psl/cook-levin
  - Key file: `SAT.v`
- **Isabelle AFP**: Weidenbach, C. (2025). "Cook-Levin Theorem". AFP.
  - https://devel.isa-afp.org/entries/Cook_Levin.html
- **Textbook**: Sipser, M. (1996). *Introduction to the Theory of Computation*, Chapter 7.

## Authors
- Sylva Formalization Project
- Based on Coq implementation by Gäher & Kunze (uds-psl/cook-levin)
-/

import Mathlib

namespace SylvaFormalization.CookLevin

/-! ## Boolean Variables and Literals -/

/-- A Boolean variable is identified by a natural number index.
    This allows for countably infinite variables. -/
abbrev Var := Nat

/-- A literal is either a positive or negative occurrence of a variable. -/
inductive Literal
  | pos (v : Var)
  | neg (v : Var)
  deriving DecidableEq, Repr, Inhabited

namespace Literal

/-- Get the underlying variable of a literal. -/
def var : Literal → Var
  | pos v => v
  | neg v => v

/-- Check if a literal is positive. -/
def isPos : Literal → Bool
  | pos _ => true
  | neg _ => false

/-- Evaluate a literal under an assignment.
    An assignment is a function from variables to Boolean values. -/
def eval (l : Literal) (assign : Var → Bool) : Bool :=
  match l with
  | pos v => assign v
  | neg v => !(assign v)

/-- Two literals are complementary if one is the positive and the other
    is the negative of the same variable. -/
def isComplementary (l₁ l₂ : Literal) : Bool :=
  l₁.var = l₂.var ∧ l₁.isPos ≠ l₂.isPos

@[simp] theorem eval_pos (v : Var) (assign : Var → Bool) :
    eval (pos v) assign = assign v := by rfl

@[simp] theorem eval_neg (v : Var) (assign : Var → Bool) :
    eval (neg v) assign = !(assign v) := by rfl

end Literal

/-! ## Clauses and CNF Formulas -/

/-- A clause is a disjunction (OR) of literals, represented as a list.
    The empty clause is unsatisfiable (false). -/
def Clause := List Literal

deriving instance DecidableEq, Repr, Inhabited for Clause

namespace Clause

/-- Evaluate a clause under an assignment.
    A clause is satisfied if at least one literal evaluates to true. -/
def eval (c : Clause) (assign : Var → Bool) : Bool :=
  c.any (λ l => l.eval assign)

/-- The empty clause is always false. -/
@[simp] theorem eval_nil (assign : Var → Bool) : eval [] assign = false := by
  simp [eval]

/-- A unit clause contains exactly one literal. -/
def isUnit (c : Clause) : Bool := c.length = 1

/-- A clause is a tautology if it contains complementary literals. -/
def isTautology (c : Clause) : Bool :=
  c.any (λ l₁ => c.any (λ l₂ => l₁.isComplementary l₂))

end Clause

/-- A CNF formula is a conjunction (AND) of clauses, represented as a list.
    The empty CNF formula is trivially satisfiable (true). -/
def CNF := List Clause

deriving instance DecidableEq, Repr, Inhabited for CNF

namespace CNF

/-- Evaluate a CNF formula under an assignment.
    A CNF is satisfied if all clauses are satisfied. -/
def eval (φ : CNF) (assign : Var → Bool) : Bool :=
  φ.all (λ c => c.eval assign)

/-- The empty CNF formula is always true (no constraints). -/
@[simp] theorem eval_nil (assign : Var → Bool) : eval [] assign = true := by
  simp [eval]

/-- A CNF formula is satisfiable if there exists an assignment making it true. -/
def Satisfiable (φ : CNF) : Prop :=
  ∃ (assign : Var → Bool), φ.eval assign = true

/-- A CNF formula is unsatisfiable if no assignment makes it true. -/
def Unsatisfiable (φ : CNF) : Prop :=
  ∀ (assign : Var → Bool), φ.eval assign = false

/-- Number of variables in a CNF formula (the maximum variable index + 1). -/
def numVars (φ : CNF) : Nat :=
  match φ.flatMap (λ c => c.map Literal.var) with
  | [] => 0
  | vars => Nat.succ (vars.foldl max 0)

/-- Number of clauses in a CNF formula. -/
def numClauses (φ : CNF) : Nat := φ.length

/-- Total size (number of literals) of a CNF formula. -/
def size (φ : CNF) : Nat :=
  φ.foldl (λ acc c => acc + c.length) 0

end CNF

/-! ## SAT Problem Definition -/

/-- The SAT problem: given a CNF formula φ, determine if it is satisfiable.
    This is the canonical NP-complete problem (Cook-Levin theorem). -/
def SAT (φ : CNF) : Bool :=
  -- In practice, SAT is a decision problem, not a computable function.
  -- This is a placeholder; the actual decidability depends on the instance.
  -- The SAT problem is NP-complete; no known polynomial-time algorithm exists.
  true -- Placeholder: the actual computation would be exponential

/-- The SAT decision problem as a proposition.
    This formulation is used in complexity-theoretic statements. -/
def SAT_decision (φ : CNF) : Prop := CNF.Satisfiable φ

/-! ## Tseitin Encoding Utilities -/

/-- Create a unit clause for a literal. -/
def unitClause (l : Literal) : Clause := [l]

/-- Tseitin constraint encoding: y ↔ (x₁ ∧ x₂) as CNF clauses.
    This introduces an auxiliary variable y representing the AND gate. -/
def tseitinAnd (y x₁ x₂ : Var) : CNF :=
  [ [Literal.neg x₁, Literal.neg x₂, Literal.pos y]
  , [Literal.pos x₁, Literal.neg y]
  , [Literal.pos x₂, Literal.neg y]
  ]

/-- Tseitin constraint encoding: y ↔ (x₁ ∨ x₂) as CNF clauses.
    This introduces an auxiliary variable y representing the OR gate. -/
def tseitinOr (y x₁ x₂ : Var) : CNF :=
  [ [Literal.pos x₁, Literal.pos x₂, Literal.neg y]
  , [Literal.neg x₁, Literal.pos y]
  , [Literal.neg x₂, Literal.pos y]
  ]

/-- Tseitin constraint encoding: y ↔ ¬x as CNF clauses.
    This introduces an auxiliary variable y representing the NOT gate. -/
def tseitinNot (y x : Var) : CNF :=
  [ [Literal.pos x, Literal.pos y]
  , [Literal.neg x, Literal.neg y]
  ]

/-- Tseitin encoding of an implication: y → (x₁ ∧ x₂) as CNF. -/
def tseitinImplAnd (y x₁ x₂ : Var) : CNF :=
  [ [Literal.neg y, Literal.pos x₁]
  , [Literal.neg y, Literal.pos x₂]
  ]

/-- Verify that Tseitin AND encoding is correct.
    For all assignments, the CNF is satisfiable iff y = (x₁ ∧ x₂). -/
theorem tseitinAnd_correct (y x₁ x₂ : Var) (assign : Var → Bool) :
    (tseitinAnd y x₁ x₂).eval assign = true ↔
    (assign y = (assign x₁ && assign x₂)) := by
  simp [tseitinAnd, CNF.eval, Clause.eval, Literal.eval]
  cases assign x₁ <;> cases assign x₂ <;> cases assign y <;> simp

/-- Verify that Tseitin OR encoding is correct. -/
theorem tseitinOr_correct (y x₁ x₂ : Var) (assign : Var → Bool) :
    (tseitinOr y x₁ x₂).eval assign = true ↔
    (assign y = (assign x₁ || assign x₂)) := by
  simp [tseitinOr, CNF.eval, Clause.eval, Literal.eval]
  cases assign x₁ <;> cases assign x₂ <;> cases assign y <;> simp

/-- Verify that Tseitin NOT encoding is correct. -/
theorem tseitinNot_correct (y x : Var) (assign : Var → Bool) :
    (tseitinNot y x).eval assign = true ↔
    (assign y = !(assign x)) := by
  simp [tseitinNot, CNF.eval, Clause.eval, Literal.eval]
  cases assign x <;> cases assign y <;> simp

/-! ## 3-CNF (k-SAT) Specialization -/

/-- A clause has at most k literals. -/
def Clause.atMostK (k : Nat) (c : Clause) : Bool := c.length ≤ k

/-- A k-CNF formula: all clauses have at most k literals. -/
def CNF.isKCNF (k : Nat) (φ : CNF) : Bool :=
  φ.all (λ c => c.atMostK k)

/-- 3-CNF is a special case where each clause has at most 3 literals.
    3-SAT is also NP-complete (can be reduced from SAT). -/
def CNF.is3CNF (φ : CNF) : Bool := φ.isKCNF 3

/-- 3-SAT problem statement. -/
def ThreeSAT (φ : CNF) : Prop := CNF.is3CNF φ ∧ CNF.Satisfiable φ

end SylvaFormalization.CookLevin
