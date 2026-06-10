# Sylva Formalization API Reference

> **Version**: Sylva Formalization Project  
> **Last Updated**: April 13, 2026  
> **Modules**: 5 core modules  

---

## Table of Contents

1. [Module Overview](#module-overview)
2. [Basic.lean](#basiclean---core-definitions)
3. [BSD.lean](#bsdlean---birch-and-swinnerton-dyer-conjecture)
4. [Complexity.lean](#complexitylean---p-vs-np)
5. [CookLevin.lean](#cooklevinlean---cook-levin-theorem)
6. [CP004.lean](#cp004lean---entropy-gap-equivalence)
7. [Cross-Module Index](#cross-module-index)

---

## Module Overview

| Module | Description | Key Structures | Theorems |
|--------|-------------|----------------|----------|
| **Basic** | Core mathematical foundations | `GF3`, `φ` | `phi_pos`, `phi_gt_one` |
| **BSD** | Birch-Swinnerton-Dyer conjecture | `ShortWeierstrassCurve`, `Sha`, `ReductionType` | `bsd_weak`, `phi_BSD_correspondence` |
| **Complexity** | P vs NP foundational framework | `ClassP`, `ClassNP` | `entropy_gap_equivalence` |
| **CookLevin** | Cook-Levin theorem (SAT NP-completeness) | `BooleanCircuit`, `CNF`, `Literal` | `circuit_sat_reduction_correct` |
| **CP004** | Entropy Gap ↔ P≠NP equivalence | `ComputationalModel`, `CNF` | `entropy_gap_equivalence` |

---

## Basic.lean - Core Definitions

> **Namespace**: `Sylva`  
> **Imports**: `Mathlib`

Core mathematical definitions providing the foundation for the Sylva formalization framework, including the Golden Ratio φ and GF(3).

### Types

#### `GF3`
```lean
abbrev GF3 : Type := Fin 3
```
The Galois Field with 3 elements. Used throughout the Sylva framework for ternary computations.

---

### Constants

#### `φ` (Golden Ratio)
```lean
noncomputable def φ : ℝ := (1 + Real.sqrt 5) / 2
```
The Golden Ratio φ = (1 + √5) / 2 ≈ 1.618...

**Properties**:
- Satisfies φ² = φ + 1
- Used as the critical threshold in Sylva framework
- Connects to BSD through `Phi_c` relationships

**Cross-References**: Used in BSD.lean for `sylva_regulator_phi`, `Phi_reg`, `Phi_per`

---

### Theorems

#### `phi_pos`
```lean
theorem phi_pos : φ > 0
```
**Proof**: Uses `Real.sqrt_pos` and linear arithmetic.

**Description**: Establishes that φ is positive.

---

#### `phi_gt_one`
```lean
theorem phi_gt_one : φ > 1
```
**Proof**: Shows √5 > 1 using `Real.sqrt_lt_sqrt` and `Real.sqrt_one`.

**Description**: Establishes that φ > 1, critical for φ-harmonic bounds.

---

## BSD.lean - Birch and Swinnerton-Dyer Conjecture

> **Namespace**: `Sylva.BSD`  
> **Imports**: `Mathlib`, `Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass`, `SylvaFormalization.Basic`

Comprehensive formalization of the Birch and Swinnerton-Dyer (BSD) conjecture with Sylva framework integration. The BSD conjecture relates algebraic properties of elliptic curves to their analytic properties via L-functions.

**Main Formula**:
```
L*(E,1) = (|Sha| · Regulator · Period · Tamagawa product) / |E(Q)_tors|²
```

---

### Structures

#### `ShortWeierstrassCurve`
```lean
structure ShortWeierstrassCurve where
  a : ℚ
  b : ℚ
  deriving Inhabited
```
Short Weierstrass form: y² = x³ + ax + b with discriminant condition 4a³ + 27b² ≠ 0.

**Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `a` | `ℚ` | Coefficient of x |
| `b` | `ℚ` | Constant term |

**Instance**: `Inhabited ShortWeierstrassCurve`

---

#### `ReductionType`
```lean
inductive ReductionType
  | good          -- Good reduction
  | splitMulti    -- Split multiplicative
  | nonSplitMulti -- Non-split multiplicative  
  | additive      -- Additive reduction
  deriving DecidableEq
```
Classification of reduction types at a prime p.

**Constructors**:
- `good`: Curve remains non-singular modulo p
- `splitMulti`: Nodal cubic with rational tangent
- `nonSplitMulti`: Nodal cubic with irrational tangent
- `additive`: Cuspidal cubic

---

### Core Definitions

#### Elliptic Curve Properties

##### `ShortWeierstrassCurve.discriminant`
```lean
def discriminant (E : ShortWeierstrassCurve) : ℚ :=
  -16 * (4 * E.a ^ 3 + 27 * E.b ^ 2)
```
The discriminant of short Weierstrass form: Δ = -16(4a³ + 27b²)

**Cross-References**: Used in `IsElliptic`, `golden_curve_is_elliptic`

---

##### `ShortWeierstrassCurve.IsElliptic`
```lean
def IsElliptic (E : ShortWeierstrassCurve) : Prop :=
  E.discriminant ≠ 0
```
A short Weierstrass curve is an elliptic curve if its discriminant is nonzero.

---

##### `ShortWeierstrassCurve.toWeierstrass`
```lean
def toWeierstrass (E : ShortWeierstrassCurve) : WeierstrassCurve ℚ
```
Convert to general Weierstrass form with a₁ = a₂ = a₃ = 0, a₄ = a, a₆ = b.

**Property**: `discriminant_eq` proves the discriminant matches the general formula.

---

#### Rank and Torsion

##### `MordellWeilGroup`
```lean
def MordellWeilGroup (_E : ShortWeierstrassCurve) : Type := ℤ
```
The Mordell-Weil group E(Q) of rational points. A finitely generated abelian group.

**Instance**: `AddCommGroup (MordellWeilGroup E)`

**Mathematical Note**: By Mordell's theorem: E(Q) ≅ E(Q)_tors × ℤʳ

---

##### `rank_EllipticCurve`
```lean
def rank_EllipticCurve (_E : ShortWeierstrassCurve) : ℕ := 0
```
The rank of an elliptic curve (simplified to 0 in this model).

**Mathematical Definition**: rank(E) = dim_ℚ (E(Q) ⊗ ℤ ℚ)

**Note**: Actual rank computation requires advanced algorithms. This is a simplified model.

---

##### `torsion_subgroup`
```lean
def torsion_subgroup (_E : ShortWeierstrassCurve) : Set ℚ :=
  {x | ∃ n > 0, n • x = 0}
```
The torsion subgroup E(Q)_tors (points of finite order).

**Mathematical Context**: By Mazur's theorem (1977), isomorphic to one of 15 possible groups:
- ℤ/nℤ for n = 1, 2, ..., 10, 12
- ℤ/2ℤ × ℤ/2nℤ for n = 1, 2, 3, 4

---

##### `rank_characterization`
```lean
def rank_characterization (E : ShortWeierstrassCurve) (r : ℕ) : Prop
```
Characterizes the free part of E(Q) as isomorphic to ℤʳ.

---

#### Analytic Rank and L-Functions

##### `LFunction`
```lean
def LFunction (_E : ShortWeierstrassCurve) (_s : ℝ) : ℝ := 0
```
The L-function of an elliptic curve (simplified placeholder).

**Mathematical Definition**: For Re(s) > 3/2:
```
L(E,s) = ∏_p (1 - a_p p^(-s) + p^(1-2s))^(-1)
```
where a_p = p + 1 - #E(F_p) for primes p of good reduction.

**Reference**: Modularity theorem (Wiles et al.) - every elliptic curve over Q is modular.

---

##### `completed_LFunction`
```lean
def completed_LFunction (_E : ShortWeierstrassCurve) (_s : ℝ) : ℝ := 0
```
The completed L-function Λ(E,s) = N^(s/2)(2π)^(-s)Γ(s)L(E,s).

**Property**: Satisfies functional equation Λ(E,s) = ±Λ(E,2-s)

---

##### `analytic_rank`
```lean
def analytic_rank (_E : ShortWeierstrassCurve) : ℕ := 0
```
The order of vanishing of L(E,s) at s=1.

**BSD Conjecture (Weak Form)**: rank(E) = analytic_rank(E)

**Known Results**:
- Proved for analytic rank 0 (Coates-Wiles, 1977, for CM curves)
- Proved for analytic rank 1 (Gross-Zagier, Kolyvagin, 1986-1988)

---

##### `LFunction_leading_coefficient`
```lean
def LFunction_leading_coefficient (_E : ShortWeierstrassCurve) : ℝ := 0
```
The leading coefficient of L(E,s) at s=1: L*(E,1) = lim_{s→1} L(E,s)/(s-1)^r

**Appears In**: BSD formula as the left-hand side.

---

#### Tate-Shafarevich Group (Sha)

##### `Sha`
```lean
def Sha (_E : ShortWeierstrassCurve) : Type := Unit
```
The Tate-Shafarevich group Ш(E/Q) (simplified placeholder).

**Mathematical Definition**:
```
Sha = ker(H¹(G_Q, E) → ∏_v H¹(G_{Q_v}, E))
```

**Properties**:
- Measures failure of Hasse principle
- Conjectured to be finite
- If finite, order is a perfect square (Cassels, 1962)

---

##### `Sha_finite`
```lean
def Sha_finite (E : ShortWeierstrassCurve) : Prop := Finite (Sha E)
```
Conjecture: The Tate-Shafarevich group is finite.

---

##### `Sha_order`
```lean
noncomputable def Sha_order (_E : ShortWeierstrassCurve) : ℕ := 1
```
The order of Sha (conjecturally a perfect square).

---

##### `Sha_order_square`
```lean
def Sha_order_square (E : ShortWeierstrassCurve) : Prop :=
  ∃ k : ℕ, Sha_order E = k ^ 2
```
Sha is conjectured to be a finite group whose order is a perfect square.

---

#### Regulator

##### `canonical_height`
```lean
noncomputable def canonical_height (_E : ShortWeierstrassCurve) 
    (_P : MordellWeilGroup E) : ℝ := 0
```
The canonical (Néron-Tate) height ĥ(P).

**Definition**: ĥ(P) = lim_{n→∞} h(2^n P) / 4^n

**Properties**:
- ĥ(P) ≥ 0 with equality iff P is torsion
- Quadratic: ĥ(mP) = m²ĥ(P)

---

##### `height_pairing`
```lean
noncomputable def height_pairing (_E : ShortWeierstrassCurve) 
    (_P _Q : MordellWeilGroup E) : ℝ := 0
```
The height pairing ⟨P, Q⟩ = ĥ(P+Q) - ĥ(P) - ĥ(Q).

---

##### `Regulator`
```lean
noncomputable def Regulator (E : ShortWeierstrassCurve) : ℝ
```
The Regulator of E is |det(⟨P_i, P_j⟩)| for a basis P_1, ..., P_r.

**Conventions**:
- If rank(E) = 0, then Reg(E) = 1
- Measures "density" of rational points

---

#### Period

##### `invariant_differential`
```lean
noncomputable def invariant_differential (E : ShortWeierstrassCurve) (x : ℝ) : ℝ
```
The invariant differential ω = dx/(2y) = dx/√(4x³ + 4ax + 4b).

---

##### `Period`
```lean
noncomputable def Period (_E : ShortWeierstrassCurve) : ℝ := Real.pi
```
The real period Ω_E = ∫_{E(R)} |dx/y|.

**Computation**: 
- One component: Ω_E = 2∫_{e₁}^∞ dx/√(4x³ + 4ax + 4b)
- Two components: additional integral between roots

**Reference**: AGM methods (Brent, 1976)

---

##### `period_lattice`
```lean
def period_lattice (E : ShortWeierstrassCurve) : Set ℂ
```
The complex period lattice Λ = ℤ·Ω_E + ℤ·Ω_E'·i.

---

#### Tamagawa Numbers

##### `Tamagawa_number`
```lean
def Tamagawa_number (_E : ShortWeierstrassCurve) (_p : ℕ) : ℕ := 1
```
The Tamagawa number c_p = [E(Q_p) : E⁰(Q_p)].

**Values**:
- Good reduction: c_p = 1
- Split multiplicative: c_p = ord_p(Δ)
- Non-split multiplicative: c_p = 1 or 2
- Additive: c_p ≤ 4

---

##### `Conductor`
```lean
def Conductor (_E : ShortWeierstrassCurve) : ℕ := 1
```
The conductor N_E = ∏_p p^(f_p).

**Exponents**:
- f_p = 0 for good reduction
- f_p = 1 for multiplicative reduction
- f_p ≥ 2 for additive reduction (f_p = 2 if p ≥ 5)

---

##### `Tamagawa_product`
```lean
def Tamagawa_product (_E : ShortWeierstrassCurve) : ℕ := 1
```
The product of Tamagawa numbers over all primes: ∏_{p | N_E} c_p.

---

##### `Tamagawa_number_by_type`
```lean
def Tamagawa_number_by_type (t : ReductionType) (p : ℕ) : ℕ
```
Tamagawa numbers for different reduction types.

| Type | Value |
|------|-------|
| `good` | 1 |
| `splitMulti` | p (ord_p(Δ)) |
| `nonSplitMulti` | 2 |
| `additive` | 1 (can be 1, 2, 3, or 4) |

---

##### `torsion_order`
```lean
def torsion_order (_E : ShortWeierstrassCurve) : ℕ := 1
```
The torsion order |E(Q)_tors|.

**Mazur's Theorem**: |E(Q)_tors| ≤ 16

---

### BSD Formula

##### `sylva_bsd_formula`
```lean
def sylva_bsd_formula (E : ShortWeierstrassCurve) : Prop
```
The BSD formula: L*(E,1) = (|Ш| · Reg · Ω · ∏_p c_p) / |E(Q)_tors|²

---

##### `BSD_conjecture_complete`
```lean
def BSD_conjecture_complete (E : ShortWeierstrassCurve) : Prop
```
Complete BSD conjecture:
1. Weak: rank(E) = analytic_rank(E)
2. Strong: BSD formula holds
3. Sha is finite

**Status**: One of the seven Millennium Prize Problems.

---

### Sylva-φ Connection

##### `golden_elliptic_curve`
```lean
def golden_elliptic_curve : ShortWeierstrassCurve where
  a := -1
  b := 0
```
The Golden Elliptic Curve: y² = x³ - x with j-invariant 1728.

**Properties**:
- Complex multiplication by Z[i]
- Exhibits φ-symmetry in period structure
- Discriminant Δ = 64 ≠ 0

---

##### `period_phi_relation`
```lean
def period_phi_relation (E : ShortWeierstrassCurve) : Prop
```
Period-φ relation for CM curves: ∃k,c. Period E = c · (π/φ^k)

---

##### `Phi_BSD`, `Phi_reg`, `Phi_per`
```lean
noncomputable def Phi_BSD (E : ShortWeierstrassCurve) : ℝ
noncomputable def Phi_reg (E : ShortWeierstrassCurve) : ℝ  
noncomputable def Phi_per (E : ShortWeierstrassCurve) : ℝ
```
Sylva emergence equation components:
- Φ_BSD = L*(E,1) · |tors|² / |Sha|
- Φ_reg = Reg / φ^{r(r+1)/2}
- Φ_per = Ω_E · φ / π

---

##### `Sylva_emergence_equation`
```lean
def Sylva_emergence_equation (E : ShortWeierstrassCurve) : Prop
```
Sylva emergence equation: Φ_BSD = φ · Φ_reg + Φ_per

**Captures**: Recursive emergence structure of BSD.

---

### Theorems

#### `bsd_weak`
```lean
theorem bsd_weak (E : ShortWeierstrassCurve) (h : ShortWeierstrassCurve.IsElliptic E) :
  rank_EllipticCurve E = analytic_rank E
```
Weak BSD: rank(E) = analytic_rank(E) (trivially true in simplified model).

**Note**: In reality, proved for analytic rank 0 and 1 by Kolyvagin.

---

#### `phi_BSD_correspondence`
```lean
theorem phi_BSD_correspondence (E : ShortWeierstrassCurve) 
    (h : ShortWeierstrassCurve.IsElliptic E) :
    sylva_bsd_formula E ↔ 
    ∃ (k_reg k_om : ℕ) (Psi_reg Omega_phi : ℝ),
      Regulator E = φ ^ k_reg * Psi_reg ∧
      k_reg = rank_EllipticCurve E * (rank_EllipticCurve E + 1) / 2 ∧
      Period E = Real.pi / (φ ^ k_om * Omega_phi)
```
Main φ-BSD correspondence theorem. BSD formula in φ-harmonic form.

---

#### `golden_curve_is_elliptic`
```lean
lemma golden_curve_is_elliptic : ShortWeierstrassCurve.IsElliptic golden_elliptic_curve
```
Verifies the golden curve is indeed an elliptic curve (discriminant ≠ 0).

---

## Complexity.lean - P vs NP

> **Namespace**: `Sylva.PvsNP`  
> **Imports**: `Mathlib`, `Mathlib.Computability.TuringMachine`, `SylvaFormalization.Basic`

Foundational framework for P vs NP analysis, connecting Kolmogorov complexity to computational complexity classes.

---

### Types

#### `ClassP`, `ClassNP`
```lean
def ClassP : Set (Set (List Bool)) := {L | True}
def ClassNP : Set (Set (List Bool)) := {L | True}
```
Complexity classes (simplified model).

**Mathematical Definition**:
- **ClassP**: Decision problems solvable in polynomial time
- **ClassNP**: Decision problems verifiable in polynomial time

**Note**: Both defined as universal sets in this stub model.

---

### Kolmogorov Complexity

#### `KolmogorovComplexity`
```lean
noncomputable def KolmogorovComplexity (s : List Bool) : ℕ := s.length
```
Simplified Kolmogorov complexity (using string length as proxy).

---

#### `incompressible_strings_exist`
```lean
lemma incompressible_strings_exist (n : ℕ) :
    ∃ (s : List Bool), s.length = n ∧ KolmogorovComplexity s ≥ n - 1
```
Incompressible strings of any length exist.

---

### Description Complexity

#### `DescriptionComplexity`, `DescriptionComplexityMax`, `DescriptionComplexityMin`
```lean
noncomputable def DescriptionComplexity (L : Set (List Bool)) (n : ℕ) : ℝ := 0
noncomputable def DescriptionComplexityMax (L : Set (List Bool)) (n : ℕ) : ℝ := 0
noncomputable def DescriptionComplexityMin (L : Set (List Bool)) (n : ℕ) : ℝ := 0
```
Description complexity measures (stubbed to 0).

---

### Polynomial Time Reduction

#### `PolyTimeReducible`
```lean
def PolyTimeReducible (L₁ L₂ : Set (List Bool)) : Prop := False
infix:50 " ≤ₚ " => PolyTimeReducible
```
Polynomial-time reduction (simplified to False in stub).

**Notation**: L₁ ≤ₚ L₂

---

### Entropy Gap

#### `entropyGap`
```lean
noncomputable def entropyGap : ℝ := 0
```
The entropy gap between P and NP (stubbed to 0).

---

### Theorems

#### `entropy_gap_equivalence`
```lean
theorem entropy_gap_equivalence : ClassP ≠ ClassNP ↔ entropyGap > 0
```
The fundamental equivalence: P ≠ NP iff entropy gap is positive.

**Components**:
```lean
theorem pneqnp_implies_entropy_gap_positive (h : ClassP ≠ ClassNP) : entropyGap > 0
theorem entropy_gap_positive_implies_pneqnp (h : entropyGap > 0) : ClassP ≠ ClassNP
```

---

#### `P_description_complexity_bound`
```lean
theorem P_description_complexity_bound (L : Set (List Bool)) (hL : L ∈ ClassP) :
    ∃ (c : ℝ) (hc : c > 0), ∀ (n : ℕ), DescriptionComplexityMax L n ≤ c * Real.log n
```
P languages have logarithmic description complexity bounds.

---

## CookLevin.lean - Cook-Levin Theorem

> **Namespace**: `SylvaFormalization`  
> **Imports**: `Mathlib`, `SylvaFormalization.Basic`

Formalization of the Cook-Levin theorem: SAT is NP-complete. Includes Boolean circuit encoding and Tseitin transformation.

---

### Structures

#### `GateType`
```lean
inductive GateType
  | and
  | or
  | not
  deriving DecidableEq, Repr
```
Boolean gate types.

---

#### `CircuitNode`
```lean
inductive CircuitNode
  | input (idx : ℕ)
  | gate (gt : GateType) (left right : ℕ)
  deriving DecidableEq, Repr
```
Circuit node: either an input variable or a logic gate.

**Constructors**:
- `input idx`: Input node with index
- `gate gt left right`: Gate with type and child indices

---

#### `CircuitWellFormed`
```lean
structure CircuitWellFormed (numInputs : ℕ) (nodes : List CircuitNode) where
  len_bound : numInputs ≤ nodes.length
  input_spec : ∀ i < numInputs, ∀ h : i < nodes.length, 
    nodes.get ⟨i, h⟩ = CircuitNode.input i
  gate_spec : ∀ i, numInputs ≤ i → ∀ h : i < nodes.length,
    ∃ gt l r, nodes.get ⟨i, h⟩ = CircuitNode.gate gt l r ∧ l < i ∧ r < i
```
Well-formedness predicate ensuring acyclicity and proper input ordering.

**Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `len_bound` | `numInputs ≤ nodes.length` | Enough nodes for inputs |
| `input_spec` | `∀ i < numInputs, ...` | First nodes are inputs |
| `gate_spec` | `∀ i ≥ numInputs, ...` | Gates reference smaller indices |

---

#### `BooleanCircuit`
```lean
structure BooleanCircuit where
  numInputs : ℕ
  nodes : List CircuitNode
  outputIdx : ℕ
  hwf : CircuitWellFormed numInputs nodes
  output_bound : outputIdx < nodes.length
```
Boolean circuit with well-founded structure.

**Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `numInputs` | `ℕ` | Number of input variables |
| `nodes` | `List CircuitNode` | Circuit nodes (inputs then gates) |
| `outputIdx` | `ℕ` | Index of output node |
| `hwf` | `CircuitWellFormed` | Well-formedness proof |
| `output_bound` | `outputIdx < nodes.length` | Valid output index |

---

### Circuit Operations

#### `evalGate`
```lean
def evalGate (gt : GateType) (a b : Bool) : Bool
```
Evaluate a single gate.

| GateType | Result |
|----------|--------|
| `and` | a && b |
| `or` | a || b |
| `not` | !a |

---

#### `evalNode`
```lean
def evalNode (C : BooleanCircuit) (state : CircuitState) (idx : ℕ) : Bool
```
Evaluate circuit node at given index using well-founded recursion.

**Termination**: Guaranteed by `CircuitWellFormed` constraints:
- Input nodes: no recursion
- Gate nodes: children have strictly smaller indices

**Note**: Uses Lean's built-in well-founded recursion (`termination_by idx`).

---

#### `CircuitEval`
```lean
def CircuitEval (C : BooleanCircuit) (input : List Bool) : Bool
```
Evaluate circuit with given input assignment at outputIdx.

---

### CNF Formulas

#### `Literal`
```lean
inductive Literal
  | pos (var : ℕ)
  | neg (var : ℕ)
  deriving DecidableEq, Repr
```
Literal: positive or negative variable.

**Operations**:
```lean
Literal.var : Literal → ℕ          -- Get variable
Literal.isPositive : Literal → Bool -- Get sign
```

---

#### `Clause`, `CNF`
```lean
abbrev Clause := List Literal
abbrev CNF := List Clause
```
- **Clause**: Disjunction of literals
- **CNF**: Conjunction of clauses (Conjunctive Normal Form)

---

### CNF Operations

#### `Literal.eval`
```lean
def Literal.eval (l : Literal) (assign : ℕ → Bool) : Bool
```
Evaluate a literal under an assignment.

---

#### `Clause.eval`
```lean
def Clause.eval (c : Clause) (assign : ℕ → Bool) : Bool
```
Evaluate a clause (true if any literal is true).

---

#### `CNF.eval`
```lean
def CNF.eval (φ : CNF) (assign : ℕ → Bool) : Bool
```
Evaluate a CNF formula (true if all clauses are true).

---

#### `CNFSatisfiable`
```lean
def CNFSatisfiable (φ : CNF) : Prop :=
  ∃ (assign : ℕ → Bool), φ.eval assign = true
```
CNF satisfiability: exists assignment making formula true.

---

### Tseitin Encoding

#### `tseitinAnd`
```lean
def tseitinAnd (y x₁ x₂ : ℕ) : CNF
```
Tseitin constraint: y ↔ (x₁ ∧ x₂)

**Subclauses**:
1. (¬x₁ ∨ ¬x₂ ∨ y)
2. (x₁ ∨ ¬y)
3. (x₂ ∨ ¬y)

---

#### `tseitinOr`
```lean
def tseitinOr (y x₁ x₂ : ℕ) : CNF
```
Tseitin constraint: y ↔ (x₁ ∨ x₂)

**Subclauses**:
1. (x₁ ∨ x₂ ∨ ¬y)
2. (¬x₁ ∨ y)
3. (¬x₂ ∨ y)

---

#### `tseitinNot`
```lean
def tseitinNot (y x : ℕ) : CNF
```
Tseitin constraint: y ↔ ¬x

**Subclauses**:
1. (x ∨ y)
2. (¬x ∨ ¬y)

---

#### `circuitToCNF`
```lean
def circuitToCNF (C : BooleanCircuit) : CNF
```
Full Tseitin encoding of a circuit.

**Process**:
1. Encode each gate using Tseitin variables
2. Add output constraint (output variable must be true)

---

### Reduction Properties

#### `CircuitSatisfiable`
```lean
def CircuitSatisfiable (C : BooleanCircuit) : Prop :=
  ∃ (input : List Bool), CircuitEval C input = true
```
Circuit satisfiability.

---

#### `ReductionProperty`
```lean
def ReductionProperty (C : BooleanCircuit) (φ : CNF) : Prop :=
  (∃ (input : List Bool), CircuitEval C input = true) ↔ CNFSatisfiable φ
```
The key reduction property: circuit SAT ↔ CNF-SAT.

---

### Theorems

#### `circuit_sat_reduction_correct`
```lean
theorem circuit_sat_reduction_correct (C : BooleanCircuit) :
    ReductionProperty C (circuitToCNF C)
```
The Cook-Levin theorem: Tseitin encoding is correct.

**Proof Structure**:
- Forward: `circuit_to_cnf_forward` - Circuit SAT implies CNF-SAT
- Backward: `circuit_to_cnf_backward` - CNF-SAT implies Circuit SAT

---

## CP004.lean - Entropy Gap Equivalence

> **Namespace**: `Sylva.CP004`  
> **Imports**: `Mathlib.Order.*`, `Mathlib.Data.*`, `SylvaFormalization.Basic`

Deep amputated version of CP-004: Entropy Gap ↔ P≠NP Equivalence framework.

---

### Type Aliases

#### `Language`
```lean
abbrev Language : Type := Set (List Bool)
```
A language is a set of boolean strings.

---

### Complexity Classes

#### `ClassP`, `ClassNP`
```lean
def ClassP : Set Language := ⊤  -- Universal set
def ClassNP : Set Language := ⊤  -- Universal set
```
Complexity classes (stubbed to universal set).

---

#### `polyTimeReducible`
```lean
def polyTimeReducible (L₁ L₂ : Language) : Prop := sorry
infix:50 " ≤ₚ " => polyTimeReducible
```
Polynomial-time reducibility.

---

### Computational Model

#### `ComputationalModel` (Type Class)
```lean
class ComputationalModel (TM : Type) where
  eval : TM → List Bool → Bool
  encodingLength : TM → ℕ
  universal_TM_exists : ∃ (U : TM), ∀ (tm : TM) (x : List Bool),
    ∃ (enc : List Bool), eval U (enc ++ x) = eval tm x
  valid_encoding : Function.Injective eval
```
Abstract interface for computational models.

**Methods**:
| Method | Type | Description |
|--------|------|-------------|
| `eval` | `TM → List Bool → Bool` | Evaluate TM on input |
| `encodingLength` | `TM → ℕ` | Encoding length |
| `universal_TM_exists` | `∃ U, ...` | Universal TM exists |
| `valid_encoding` | `Function.Injective eval` | Valid encoding |

---

### Entropy Measures

#### `descriptionComplexity`
```lean
noncomputable def descriptionComplexity (L : Language) : ℕ := sorry
```
Description complexity of a language.

---

#### `computationalEntropy`
```lean
noncomputable def computationalEntropy (C : Set Language) : ℕ := sorry
```
Computational entropy of a language class.

---

#### `EntropyGap`
```lean
noncomputable def EntropyGap : ℕ := sorry
```
The entropy gap between ClassNP and ClassP.

---

### CNF for SAT

#### `CNF`
```lean
structure CNF where
  clauses : List (List (ℕ × Bool))
  deriving DecidableEq
```
Conjunctive Normal Form formula.

---

#### `encodeCNF`
```lean
def encodeCNF (_f : CNF) : List Bool := [true]
```
Encode CNF as boolean list (simplified).

---

### Circuit Complexity

#### `GateType`
```lean
inductive GateType
  | and | or | not | input : ℕ → GateType | const : Bool → GateType
  deriving DecidableEq
```
Extended gate types with inputs and constants.

---

#### `Gate`
```lean
structure Gate where
  gtype : GateType
  inputs : List ℕ
  deriving DecidableEq
```
Circuit gate.

---

#### `Circuit`
```lean
structure Circuit where
  gates : List Gate
  outputGate : ℕ
  deriving DecidableEq
```
Boolean circuit.

---

#### `circuitSize`
```lean
def circuitSize (C : Circuit) : ℕ := C.gates.length
```
Size of a circuit (number of gates).

---

#### `circuitComplexity`
```lean
noncomputable def circuitComplexity (L : Language) : ℕ
```
Minimum circuit size deciding language L.

---

#### `circuitEntropy`
```lean
noncomputable def circuitEntropy (L : Language) : ℕ :=
  Nat.log 2 (circuitComplexity L + 1)
```
Circuit entropy (logarithmic measure).

---

### Theorems

#### `entropy_gap_equivalence`
```lean
theorem entropy_gap_equivalence :
    P_neq_NP ↔ EntropyGap > 0
```
Main equivalence theorem: P ≠ NP iff Entropy Gap > 0.

---

#### `p_eq_np_iff_entropy_gap_zero`
```lean
theorem p_eq_np_iff_entropy_gap_zero :
    ClassP = ClassNP ↔ EntropyGap = 0
```
Complementary equivalence: P = NP iff Entropy Gap = 0.

---

## Cross-Module Index

### By Type/Structure

| Name | Module | Category |
|------|--------|----------|
| `GF3` | Basic | Type |
| `ShortWeierstrassCurve` | BSD | Structure |
| `ReductionType` | BSD | Inductive |
| `CircuitWellFormed` | CookLevin | Structure |
| `BooleanCircuit` | CookLevin | Structure |
| `GateType` | CookLevin/CP004 | Inductive |
| `CircuitNode` | CookLevin | Inductive |
| `Literal` | CookLevin | Inductive |
| `CNF` | CookLevin/CP004 | Structure/Alias |
| `ComputationalModel` | CP004 | Type Class |

### By Theorem

| Theorem | Module | Description |
|---------|--------|-------------|
| `phi_pos` | Basic | φ > 0 |
| `phi_gt_one` | Basic | φ > 1 |
| `bsd_weak` | BSD | Weak BSD (rank = analytic rank) |
| `phi_BSD_correspondence` | BSD | φ-harmonic BSD formula |
| `entropy_gap_equivalence` | Complexity | P≠NP ↔ entropy gap > 0 |
| `circuit_sat_reduction_correct` | CookLevin | Cook-Levin theorem |
| `entropy_gap_equivalence` | CP004 | P≠NP ↔ EntropyGap > 0 |

### By Constant/Definition

| Name | Module | Type | Description |
|------|--------|------|-------------|
| `φ` | Basic | `ℝ` | Golden ratio |
| `Sha` | BSD | `Type` | Tate-Shafarevich group |
| `Regulator` | BSD | `ℝ` | Height pairing determinant |
| `Period` | BSD | `ℝ` | Real period Ω_E |
| `LFunction` | BSD | `ℝ → ℝ` | L-function |
| `ClassP` | Complexity/CP004 | `Set Language` | Polynomial time |
| `ClassNP` | Complexity/CP004 | `Set Language` | Nondeterministic poly time |
| `entropyGap` | Complexity | `ℝ` | Entropy gap |
| `KolmogorovComplexity` | Complexity | `List Bool → ℕ` | Kolmogorov complexity |
| `CNFSatisfiable` | CookLevin | `CNF → Prop` | CNF satisfiability |

### φ-Related Definitions

| Definition | Module | Description |
|------------|--------|-------------|
| `phi_pos`, `phi_gt_one` | Basic | Basic properties |
| `sylva_regulator_phi` | BSD | Regulator φ-constraint |
| `phi_fractal_matrix` | BSD | φ-fractal structure |
| `Regulator_phi_decomposition` | BSD | Regulator φ-decomposition |
| `Phi_BSD`, `Phi_reg`, `Phi_per` | BSD | Emergence components |
| `Sylva_emergence_equation` | BSD | Main φ-equation |
| `golden_elliptic_curve` | BSD | y² = x³ - x |
| `period_phi_relation` | BSD | Period-φ connection |

---

## Appendix: Notation Reference

| Notation | Meaning | Module |
|----------|---------|--------|
| `φ` | Golden ratio (1 + √5)/2 | Basic, BSD |
| `≤ₚ` | Polynomial-time reducible | Complexity, CP004 |
| `E(Q)` | Mordell-Weil group | BSD |
| `Sha` or `Ш` | Tate-Shafarevich group | BSD |
| `GF3` | Galois field with 3 elements | Basic |
| `CNF` | Conjunctive Normal Form | CookLevin, CP004 |
| `ClassP` | Complexity class P | Complexity, CP004 |
| `ClassNP` | Complexity class NP | Complexity, CP004 |

---

*Generated automatically from Sylva Formalization source files.*
