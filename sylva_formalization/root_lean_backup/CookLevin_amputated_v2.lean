import Mathlib

namespace Sylva

inductive GateType
  | and | or | not
  deriving DecidableEq, Repr

inductive CircuitNode
  | input (idx : ℕ)
  | gate (gt : GateType) (left right : ℕ)
  deriving DecidableEq, Repr

structure CircuitWf (nodes : List CircuitNode) (numInputs : ℕ) where
  input_spec : ∀ idx (_h1 : idx < numInputs) (_h2 : idx < nodes.length),
    nodes.get ⟨idx, _h2⟩ = CircuitNode.input idx
  gate_spec : ∀ idx (_h1 : idx ≥ numInputs) (_h2 : idx < nodes.length),
    ∃ gt l r, nodes.get ⟨idx, _h2⟩ = CircuitNode.gate gt l r ∧ l < idx ∧ r < idx

structure BooleanCircuit where
  numInputs : ℕ
  nodes : List CircuitNode
  hwf : CircuitWf nodes numInputs
  deriving DecidableEq

def evalGate (gt : GateType) (a b : Bool) : Bool :=
  match gt with | GateType.and => a && b | GateType.or => a || b | GateType.not => !a

def evalNode (C : BooleanCircuit) (state : List Bool) (idx : ℕ) : Bool :=
  if h : idx < C.numInputs then
    if h2 : idx < state.length then state.get ⟨idx, h2⟩ else false
  else if h2 : idx < C.nodes.length then
    have _h3 : idx ≥ C.numInputs := by omega
    match h5 : C.nodes.get ⟨idx, h2⟩ with
    | CircuitNode.input _ => false
    | CircuitNode.gate gt l r =>
      have hl : l < idx := by
        have h4 := C.hwf.gate_spec idx _h3 h2
        rcases h4 with ⟨gt', l', r', h_eq, hl', hr'⟩
        rw [h5] at h_eq
        simp at h_eq
        omega
      have hr : r < idx := by
        have h4 := C.hwf.gate_spec idx _h3 h2
        rcases h4 with ⟨gt', l', r', h_eq, hl', hr'⟩
        rw [h5] at h_eq
        simp at h_eq
        omega
      evalGate gt (evalNode C state l) (evalNode C state r)
  else
    false
termination_by idx

def evalCircuit (C : BooleanCircuit) (input : List Bool) : Bool :=
  evalNode C input (C.nodes.length - 1)

inductive Literal | pos (var : ℕ) | neg (var : ℕ) deriving DecidableEq, Repr

def Literal.var : Literal → ℕ | pos v => v | neg v => v
def Literal.isPositive : Literal → Bool | pos _ => true | neg _ => false
def Literal.eval (assign : ℕ → Bool) : Literal → Bool | pos v => assign v | neg v => !(assign v)

def Clause := List Literal
def Clause.eval (assign : ℕ → Bool) (c : Clause) : Bool := c.any (fun lit => lit.eval assign)

def CNF := List Clause
def CNF.eval (assign : ℕ → Bool) (cnf : CNF) : Bool := cnf.all (fun c => c.eval assign)
def CNF.satisfiable (cnf : CNF) : Prop := ∃ assign, cnf.eval assign = true

def gateCnf (idx : ℕ) (gt : GateType) (l r : ℕ) : CNF :=
  match gt with
  | GateType.and =>
    [[Literal.neg l, Literal.neg r, Literal.pos idx],
     [Literal.pos l, Literal.neg idx],
     [Literal.pos r, Literal.neg idx]]
  | GateType.or =>
    [[Literal.pos l, Literal.pos r, Literal.neg idx],
     [Literal.neg l, Literal.pos idx],
     [Literal.neg r, Literal.pos idx]]
  | GateType.not =>
    [[Literal.neg l, Literal.neg idx],
     [Literal.pos l, Literal.pos idx]]

def circuitToCnf (C : BooleanCircuit) : CNF :=
  let gateClauses := (List.zip (List.range C.nodes.length) C.nodes).flatMap (fun ⟨idx, node⟩ =>
    match node with
    | CircuitNode.input _ => []
    | CircuitNode.gate gt l r => gateCnf idx gt l r
  )
  [Literal.pos (C.nodes.length - 1)] :: gateClauses

-- Gate CNF is satisfied iff the assignment matches the gate evaluation
lemma gateCnf_satisfied_iff (idx : ℕ) (gt : GateType) (l r : ℕ) (assign : ℕ → Bool) :
    CNF.eval assign (gateCnf idx gt l r) = true ↔
    assign idx = evalGate gt (assign l) (assign r) := by
  cases gt with
  | and =>
    simp [gateCnf, CNF.eval, Clause.eval, Literal.eval, evalGate]
    have h_and : assign idx = (assign l && assign r) ↔
      (assign l = false ∨ assign r = false ∨ assign idx = true) ∧
      (assign l = true ∨ assign idx = false) ∧
      (assign r = true ∨ assign idx = false) := by
      cases assign l <;> cases assign r <;> cases assign idx <;> simp
    rw [h_and]
  | or =>
    simp [gateCnf, CNF.eval, Clause.eval, Literal.eval, evalGate]
    have h_or : assign idx = (assign l || assign r) ↔
      (assign l = true ∨ assign r = true ∨ assign idx = false) ∧
      (assign l = false ∨ assign idx = true) ∧
      (assign r = false ∨ assign idx = true) := by
      cases assign l <;> cases assign r <;> cases assign idx <;> simp
    rw [h_or]
  | not =>
    simp [gateCnf, CNF.eval, Clause.eval, Literal.eval, evalGate]
    have h_not : assign idx = !assign l ↔
      (assign l = false ∨ assign idx = false) ∧
      (assign l = true ∨ assign idx = true) := by
      cases assign l <;> cases assign idx <;> simp
    rw [h_not]

-- Helper: evalNode on a gate computes the gate function
lemma evalNode_gate (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (h2 : idx < C.nodes.length) (h3 : idx ≥ C.numInputs)
    (gt : GateType) (l r : ℕ) (h5 : C.nodes.get ⟨idx, h2⟩ = CircuitNode.gate gt l r) :
    evalNode C state idx = evalGate gt (evalNode C state l) (evalNode C state r) := by sorry

-- Key lemma: strong induction on node index showing assignment equals evalNode
lemma evalNode_eq_of_assign (C : BooleanCircuit) (assign : ℕ → Bool) (input : List Bool)
    (hlen : input.length = C.numInputs)
    (hinput : ∀ i, i < C.numInputs → assign i = input.get ⟨i, sorry⟩)
    (hgate : ∀ i, i ≥ C.numInputs → i < C.nodes.length →
      match C.nodes.get ⟨i, sorry⟩ with
      | CircuitNode.input _ => True
      | CircuitNode.gate gt l r => assign i = evalGate gt (assign l) (assign r)) :
    ∀ i, i < C.nodes.length → evalNode C input i = assign i := by sorry

-- Helper: length of zip with range equals length of list
lemma zip_length (n : ℕ) (xs : List α) (h : n = xs.length) :
    (List.zip (List.range n) xs).length = xs.length := by
  rw [List.length_zip]
  simp [List.length_range, h]

-- Helper: get element from zip with range
lemma zip_get (n : ℕ) (xs : List α) (h : n = xs.length) (k : ℕ)
    (hk : k < xs.length) :
    (List.zip (List.range n) xs).get ⟨k, sorry⟩ =
    (k, xs.get ⟨k, hk⟩) := by sorry

-- Helper: membership in zip implies get relationship
lemma mem_zip_implies_get (n : ℕ) (xs : List α) (h : n = xs.length) (idx : ℕ) (node : α)
    (hp : (idx, node) ∈ List.zip (List.range n) xs) :
    ∃ (h_get : idx < xs.length), xs.get ⟨idx, h_get⟩ = node := by sorry

-- The gate clauses in circuitToCnf are satisfied iff all gate constraints hold
lemma circuitToCnf_gates (C : BooleanCircuit) (assign : ℕ → Bool) :
    CNF.eval assign ((List.zip (List.range C.nodes.length) C.nodes).flatMap
      (fun ⟨idx, node⟩ =>
        match node with
        | CircuitNode.input _ => []
        | CircuitNode.gate gt l r => gateCnf idx gt l r)) = true ↔
    ∀ i, i ≥ C.numInputs → i < C.nodes.length →
      match C.nodes.get ⟨i, sorry⟩ with
      | CircuitNode.input _ => True
      | CircuitNode.gate gt l r => assign i = evalGate gt (assign l) (assign r) := by sorry

theorem circuitSat_NPC (C : BooleanCircuit) :
    (∃ input : List Bool, input.length = C.numInputs ∧ evalCircuit C input = true) ↔
    CNF.satisfiable (circuitToCnf C) := by sorry

theorem tseitin_correct (C : BooleanCircuit) (input : List Bool) (_hlen : input.length = C.numInputs) :
    CNF.eval (fun v => if v < C.nodes.length then evalNode C input v else false) (circuitToCnf C) = true ↔
    evalCircuit C input = true := by sorry

end Sylva
