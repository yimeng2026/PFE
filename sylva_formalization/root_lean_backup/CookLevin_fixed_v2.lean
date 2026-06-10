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
    evalNode C state idx = evalGate gt (evalNode C state l) (evalNode C state r) := by
  delta evalNode
  simp only [h3, h2, h5]

-- Key lemma: strong induction on node index showing assignment equals evalNode
lemma evalNode_eq_of_assign (C : BooleanCircuit) (assign : ℕ → Bool) (input : List Bool)
    (hlen : input.length = C.numInputs)
    (hinput : ∀ i, i < C.numInputs → assign i = input.get ⟨i, by omega⟩)
    (hgate : ∀ i, i ≥ C.numInputs → i < C.nodes.length →
      match C.nodes.get ⟨i, by omega⟩ with
      | CircuitNode.input _ => True
      | CircuitNode.gate gt l r => assign i = evalGate gt (assign l) (assign r)) :
    ∀ i, i < C.nodes.length → evalNode C input i = assign i := by
  intro i hi
  induction' i using Nat.strongRecOn with i ih
  by_cases h : i < C.numInputs
  · -- Input node
    have h_i : i < input.length := by omega
    delta evalNode
    simp only [h, h_i]
    exact hinput i h
  · -- Gate node
    have h3 : i ≥ C.numInputs := Nat.ge_of_not_lt h
    rcases C.hwf.gate_spec i h3 hi with ⟨gt, l, r, h_eq, hl, hr⟩
    have h_eq' := evalNode_gate C input i hi h3 gt l r h_eq
    rw [h_eq']
    have h_gate := hgate i h3 hi
    rw [h_eq] at h_gate
    have h_l : evalNode C input l = assign l := ih l hl (by linarith)
    have h_r : evalNode C input r = assign r := ih r hr (by linarith)
    rw [h_l, h_r]
    exact h_gate.symm

-- Helper: gate nodes are at indices >= numInputs
lemma gate_index_ge_numInputs (C : BooleanCircuit) (idx : ℕ) (h : idx < C.nodes.length)
    (gt : GateType) (l r : ℕ) (h_eq : C.nodes.get ⟨idx, h⟩ = CircuitNode.gate gt l r) :
    idx ≥ C.numInputs := by
  by_contra h'
  push_neg at h'
  have h_input := C.hwf.input_spec idx h' h
  rw [h_eq] at h_input
  contradiction

-- Helper: length of zip with range equals length of list
lemma zip_length (n : ℕ) (xs : List α) (h : n = xs.length) :
    (List.zip (List.range n) xs).length = xs.length := by
  rw [List.length_zip]
  simp [List.length_range, h]

-- Helper: get element from zip with range
lemma zip_get (n : ℕ) (xs : List α) (h : n = xs.length) (k : ℕ)
    (hk : k < xs.length) :
    (List.zip (List.range n) xs).get ⟨k, by
      have hlen : (List.zip (List.range n) xs).length = xs.length := by
        simp [List.length_zip, List.length_range, h]
      linarith⟩ =
    (k, xs.get ⟨k, hk⟩) := by
  simp [List.get_eq_getElem, List.zip_eq_zipWith, List.getElem_zipWith, List.getElem_range]
  all_goals
    rw [List.length_zipWith]
    simp [List.length_range, h]
    omega

-- Helper: membership in zip implies get relationship
lemma mem_zip_implies_get (n : ℕ) (xs : List α) (h : n = xs.length) (idx : ℕ) (node : α)
    (hp : (idx, node) ∈ List.zip (List.range n) xs) :
    ∃ (h_get : idx < xs.length), xs.get ⟨idx, h_get⟩ = node := by
  rw [List.mem_iff_get] at hp
  rcases hp with ⟨k, hk⟩
  have hk2 : k.1 < xs.length := by
    have hlen : (List.zip (List.range n) xs).length = xs.length := by
      simp [List.length_zip, List.length_range, h]
    have : k.1 < (List.zip (List.range n) xs).length := k.2
    linarith
  have h_eq : (List.zip (List.range n) xs).get k = (idx, node) := hk
  have h_eq2 : (List.zip (List.range n) xs).get k = (k.1, xs.get ⟨k.1, hk2⟩) := by
    simp [List.get_eq_getElem, List.zip_eq_zipWith, List.getElem_zipWith, List.getElem_range]
    all_goals
      rw [List.length_zipWith]
      simp [List.length_range, h]
      omega
  rw [h_eq2] at h_eq
  injection h_eq with h1 h2
  use hk2
  rw [h1] at h2
  exact h2.symm

-- The gate clauses in circuitToCnf are satisfied iff all gate constraints hold
lemma circuitToCnf_gates (C : BooleanCircuit) (assign : ℕ → Bool) :
    CNF.eval assign ((List.zip (List.range C.nodes.length) C.nodes).flatMap
      (fun ⟨idx, node⟩ =>
        match node with
        | CircuitNode.input _ => []
        | CircuitNode.gate gt l r => gateCnf idx gt l r)) = true ↔
    ∀ i, i ≥ C.numInputs → i < C.nodes.length →
      match C.nodes.get ⟨i, by omega⟩ with
      | CircuitNode.input _ => True
      | CircuitNode.gate gt l r => assign i = evalGate gt (assign l) (assign r) := by
  simp [CNF.eval, List.all_flatMap, List.all_eq_true]
  constructor
  · -- Forward
    intro h i hge hi
    let node := C.nodes.get ⟨i, hi⟩
    have h_mem : (i, node) ∈ List.zip (List.range C.nodes.length) C.nodes := by
      rw [List.mem_iff_get]
      use ⟨i, by rw [zip_length C.nodes.length C.nodes rfl]; exact hi⟩
      rw [zip_get C.nodes.length C.nodes rfl i hi]
      simp
    have h_all := h i node h_mem
    cases node with
    | input _ => simp at h_all ⊢; trivial
    | gate gt l r =>
      simp at h_all
      rw [gateCnf_satisfied_iff] at h_all
      simpa using h_all
  · -- Backward
    intro h idx node h_mem
    have h_node := mem_zip_implies_get C.nodes.length C.nodes rfl idx node h_mem
    rcases h_node with ⟨h_get, h_eq⟩
    cases C.nodes.get ⟨idx, h_get⟩ with
    | input _ =>
      simp [h_eq]
      trivial
    | gate gt l r =>
      have hge : idx ≥ C.numInputs := gate_index_ge_numInputs C idx h_get gt l r (by rw [h_eq])
      have h_all := h idx hge h_get
      simp [h_eq] at h_all
      simp [h_eq]
      rw [gateCnf_satisfied_iff]
      exact h_all.symm

theorem circuitSat_NPC (C : BooleanCircuit) :
    (∃ input : List Bool, input.length = C.numInputs ∧ evalCircuit C input = true) ↔
    CNF.satisfiable (circuitToCnf C) := by
  constructor
  · -- Forward: circuit → CNF
    rintro ⟨input, hlen, heval⟩
    use fun v => if v < C.nodes.length then evalNode C input v else false
    simp [CNF.satisfiable, CNF.eval, circuitToCnf]
    constructor
    · -- Output clause
      simp [Clause.eval, Literal.eval, evalCircuit]
      cases h : C.nodes.length with
      | zero =>
        simp [evalCircuit, evalNode] at heval
      | succ n =>
        have hlast : n < C.nodes.length := by omega
        simp [hlast] at heval
        simpa using heval
    · -- Gate clauses
      rw [circuitToCnf_gates]
      intro i hge hi
      cases C.nodes.get ⟨i, hi⟩ with
      | input _ => simp
      | gate gt l r =>
        have h_eq : evalNode C input i = evalGate gt (evalNode C input l) (evalNode C input r) := by
          apply evalNode_gate
          all_goals assumption
        simp [h_eq]
  · -- Backward: CNF → circuit
    rintro ⟨assign, heval⟩
    let input := (List.range C.numInputs).map (fun i => assign i)
    have hlen : input.length = C.numInputs := by simp [input]
    use input, hlen
    simp [evalCircuit]
    have hout := heval
    simp [CNF.eval, circuitToCnf] at hout
    rcases hout with ⟨hout, hgates⟩
    simp [Clause.eval, Literal.eval] at hout
    have h1 : C.nodes.length - 1 < C.nodes.length ∨ C.nodes.length = 0 := by
      cases C.nodes.length with
      | zero => right; rfl
      | succ n => left; omega
    cases h1 with
    | inl hlt =>
      have hout' : assign (C.nodes.length - 1) = true := by
        simp [hlt] at hout
        exact hout
      have heval_eq : evalNode C input (C.nodes.length - 1) = assign (C.nodes.length - 1) := by
        apply evalNode_eq_of_assign
        · exact hlen
        · intro i hi
          simp [input]
          have : i < (List.range C.numInputs).length := by
            simp; omega
          rw [List.get_map _ _ ⟨i, this⟩]
          simp
        · rw [circuitToCnf_gates] at hgates
          exact hgates
      rw [heval_eq, hout']
    | inr hzero =>
      simp [hzero, evalNode]

theorem tseitin_correct (C : BooleanCircuit) (input : List Bool) (_hlen : input.length = C.numInputs) :
    CNF.eval (fun v => if v < C.nodes.length then evalNode C input v else false) (circuitToCnf C) = true ↔
    evalCircuit C input = true := by
  simp [evalCircuit, CNF.eval, circuitToCnf]
  constructor
  · -- Forward: CNF true → circuit true
    intro h
    rcases h with ⟨hout, hgates⟩
    simp [Clause.eval, Literal.eval] at hout
    cases h : C.nodes.length with
    | zero =>
      simp [evalNode]
    | succ n =>
      have hlast : n < C.nodes.length := by omega
      simp [hlast] at hout
      simpa using hout
  · -- Backward: circuit true → CNF true
    intro heval
    constructor
    · -- Output clause
      simp [Clause.eval, Literal.eval]
      cases h : C.nodes.length with
      | zero =>
        simp [evalCircuit, evalNode] at heval
      | succ n =>
        have hlast : n < C.nodes.length := by omega
        simp [hlast] at heval
        simpa using heval
    · -- Gate clauses
      rw [circuitToCnf_gates]
      intro i hge hi
      cases C.nodes.get ⟨i, hi⟩ with
      | input _ => simp
      | gate gt l r =>
        have h_eq : evalNode C input i = evalGate gt (evalNode C input l) (evalNode C input r) := by
          apply evalNode_gate
          all_goals assumption
        simp [h_eq]

end Sylva
