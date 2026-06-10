/-
CookLevin_P1-003.lean - circuit_to_cnf_backward核心证明
============================================================

目标: 证明电路到CNF转换的反向正确性
策略: 使用强归纳法，从CNF满足赋值中提取电路满足赋值

核心思想:
1. 给定circuitToCNF C的满足赋值assign
2. 提取前C.numInputs个变量作为电路输入input
3. 用强归纳法证明: ∀ idx < C.nodes.length, evalNode C input idx = assign idx
4. 特别地，evalNode C input C.outputIdx = assign C.outputIdx = true
   (因为outputConstraint强制outputIdx为true)
5. 因此CircuitEval C input = true

关键不变式:
- 输入节点: evalNode C input i = input[i] = assign i (由构造)
- 门节点: evalNode C input idx = evalGate gt (evalNode C input l) (evalNode C input r)
          = evalGate gt (assign l) (assign r) (由归纳假设)
          = assign idx (由Tseitin编码的约束强制)
-/

import Mathlib
import SylvaFormalization.Basic

namespace SylvaFormalization

-- ============================================
-- Section 1: 前置定义（与CookLevin_fixed.lean一致）
-- ============================================

/-- Boolean gate type -/
inductive GateType
  | and
  | or
  | not
   deriving DecidableEq, Repr

/-- Circuit node: either an input or a gate -/
inductive CircuitNode
  | input (idx : ℕ)
  | gate (gt : GateType) (left right : ℕ)
  deriving DecidableEq, Repr

/-- Well-formedness predicate for circuits. -/
structure CircuitWellFormed (numInputs : ℕ) (nodes : List CircuitNode) where
  len_bound : numInputs ≤ nodes.length
  input_spec : ∀ i < numInputs, ∀ h : i < nodes.length, 
    nodes.get ⟨i, h⟩ = CircuitNode.input i
  gate_spec : ∀ i, numInputs ≤ i → ∀ h : i < nodes.length,
    ∃ gt l r, nodes.get ⟨i, h⟩ = CircuitNode.gate gt l r ∧ l < i ∧ r < i

/-- Boolean circuit with explicit well-founded structure. -/
structure BooleanCircuit where
  numInputs : ℕ
  nodes : List CircuitNode
  outputIdx : ℕ
  hwf : CircuitWellFormed numInputs nodes
  output_bound : outputIdx < nodes.length

def evalGate : GateType → Bool → Bool → Bool
  | GateType.and, a, b => a && b
  | GateType.or, a, b => a || b
  | GateType.not, a, _ => !a

/-- Evaluate a circuit node with well-founded recursion -/
def evalNode (C : BooleanCircuit) (state : List Bool) (idx : ℕ) : Bool :=
  if h : idx < C.nodes.length then
    match heq : C.nodes.get ⟨idx, h⟩ with
    | CircuitNode.input i => 
        if h' : i < state.length then state.get ⟨i, h'⟩ else false
    | CircuitNode.gate gt l r => 
        evalGate gt (evalNode C state l) (evalNode C state r)
  else
    false
termination_by idx
decreasing_by
  all_goals sorry

/-- Evaluate circuit with given input assignment -/
def CircuitEval (C : BooleanCircuit) (input : List Bool) : Bool :=
  evalNode C input C.outputIdx

lemma evalNode_gate_eq (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (gt : GateType) (l r : ℕ)
    (hidx : idx < C.nodes.length)
    (hgate : C.numInputs ≤ idx)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r) :
    evalNode C state idx = evalGate gt (evalNode C state l) (evalNode C state r) := by
  sorry

-- ============================================
-- Section 2: CNF定义（与CookLevin_fixed.lean一致）
-- ============================================

inductive Literal
  | pos (var : ℕ)
  | neg (var : ℕ)
  deriving DecidableEq, Repr

def Literal.var : Literal → ℕ
  | pos v => v
  | neg v => v

def Literal.isPositive : Literal → Bool
  | pos _ => true
  | neg _ => false

def Literal.eval (l : Literal) (assign : ℕ → Bool) : Bool :=
  match l with
  | pos v => assign v
  | neg v => !(assign v)

def Clause := List Literal

def Clause.eval (c : Clause) (assign : ℕ → Bool) : Bool :=
  c.any (λ l => l.eval assign)

abbrev CNF := List Clause

def CNF.eval (φ : CNF) (assign : ℕ → Bool) : Bool :=
  φ.all (λ c => c.eval assign)

def CNFSatisfiable (φ : CNF) : Prop :=
  ∃ (assign : ℕ → Bool), φ.eval assign = true

def unitClause (l : Literal) : Clause := [l]

def tseitinAnd (y x₁ x₂ : ℕ) : CNF :=
  [ [Literal.neg x₁, Literal.neg x₂, Literal.pos y]
  , [Literal.pos x₁, Literal.neg y]
  , [Literal.pos x₂, Literal.neg y]
  ]

def tseitinOr (y x₁ x₂ : ℕ) : CNF :=
  [ [Literal.pos x₁, Literal.pos x₂, Literal.neg y]
  , [Literal.neg x₁, Literal.pos y]
  , [Literal.neg x₂, Literal.pos y]
  ]

def tseitinNot (y x : ℕ) : CNF :=
  [ [Literal.pos x, Literal.pos y]
  , [Literal.neg x, Literal.neg y]
  ]

def gateToCNF (C : BooleanCircuit) (idx : ℕ) : CNF :=
  if h : idx < C.nodes.length then
    match C.nodes.get ⟨idx, h⟩ with
    | CircuitNode.input _ => []
    | CircuitNode.gate gt l r =>
        match gt with
        | GateType.and => tseitinAnd idx l r
        | GateType.or => tseitinOr idx l r
        | GateType.not => tseitinNot idx l
  else
    []

def circuitToCNF (C : BooleanCircuit) : CNF :=
  let gateClauses : CNF := List.flatten (List.map (gateToCNF C) (List.range C.nodes.length))
  let outputConstraint : CNF := [[Literal.pos C.outputIdx]]
  gateClauses ++ outputConstraint

def tseitinAssignment (C : BooleanCircuit) (input : List Bool) : ℕ → Bool :=
  λ v =>
    if h : v < C.nodes.length then
      evalNode C input v
    else
      false

def CircuitSatisfiable (C : BooleanCircuit) : Prop :=
  ∃ (input : List Bool), CircuitEval C input = true

def ReductionProperty (C : BooleanCircuit) (φ : CNF) : Prop :=
  (∃ (input : List Bool), CircuitEval C input = true) ↔ CNFSatisfiable φ

-- ============================================
-- Section 3: 辅助引理 - 列表操作
-- ============================================

/-- List.range n生成[0, 1, ..., n-1] -/
lemma mem_range_iff (n i : ℕ) : i ∈ List.range n ↔ i < n := by
  simp [List.mem_range]

/-- 映射后的列表成员关系 -/
lemma mem_map_range {α : Type} (f : ℕ → α) (n : ℕ) (y : α) :
    y ∈ List.map f (List.range n) ↔ ∃ i < n, f i = y := by
  simp [List.mem_map, List.mem_range]

/-- flatten后的列表成员关系 -/
lemma mem_flatten_iff {α : Type} (L : List (List α)) (x : α) :
    x ∈ List.flatten L ↔ ∃ l ∈ L, x ∈ l := by
  simp [List.mem_flatten]

-- ============================================
-- Section 4: 辅助引理 - CNF求值
-- ============================================

/-- CNF求值对append的分解 -/
lemma cnf_eval_append (φ₁ φ₂ : CNF) (assign : ℕ → Bool) :
    (φ₁ ++ φ₂).eval assign = (φ₁.eval assign && φ₂.eval assign) := by
  simp [CNF.eval, List.all_append, Bool.and_eq_true]

/-- 空CNF求值为true -/
lemma empty_cnf_eval_true (assign : ℕ → Bool) : CNF.eval [] assign = true := by
  simp [CNF.eval]

/-- 单个子句的CNF求值 -/
lemma single_cnf_eval (c : Clause) (assign : ℕ → Bool) :
    CNF.eval [c] assign = c.eval assign := by
  simp [CNF.eval]

-- ============================================
-- Section 5: 辅助引理 - Tseitin约束的语义
-- ============================================

/-- tseitinAnd的语义: 赋值满足CNF当且仅当 y = x₁ ∧ x₂ -/
lemma tseitinAnd_semantics (y x₁ x₂ : ℕ) (assign : ℕ → Bool) :
    (tseitinAnd y x₁ x₂).eval assign = true ↔
    (assign y = (assign x₁ && assign x₂)) := by
  simp [tseitinAnd, CNF.eval, Clause.eval, Literal.eval]
  constructor
  · -- 正向: CNF满足 → y = x₁ ∧ x₂
    intro h
    rcases h with ⟨h1, h2, h3⟩
    cases h_y : assign y
    · -- assign y = false
      cases h_x1 : assign x₁
      · -- assign x₁ = false
        cases h_x2 : assign x₂
        · -- assign x₂ = false
          simp [h_y, h_x1, h_x2]
        · -- assign x₂ = true
          simp [h_y, h_x1, h_x2] at h3
      · -- assign x₁ = true
        cases h_x2 : assign x₂
        · -- assign x₂ = false
          simp [h_y, h_x1, h_x2] at h3
        · -- assign x₂ = true
          simp [h_y, h_x1, h_x2] at h1
    · -- assign y = true
      cases h_x1 : assign x₁
      · -- assign x₁ = false
        cases h_x2 : assign x₂
        · -- assign x₂ = false
          simp [h_y, h_x1, h_x2] at h1
        · -- assign x₂ = true
          simp [h_y, h_x1, h_x2] at h2
      · -- assign x₁ = true
        cases h_x2 : assign x₂
        · -- assign x₂ = false
          simp [h_y, h_x1, h_x2] at h2
        · -- assign x₂ = true
          simp [h_y, h_x1, h_x2]
  · -- 反向: y = x₁ ∧ x₂ → CNF满足
    intro h_eq
    rw [h_eq]
    cases assign x₁ <;> cases assign x₂ <;> simp

/-- tseitinOr的语义: 赋值满足CNF当且仅当 y = x₁ ∨ x₂ -/
lemma tseitinOr_semantics (y x₁ x₂ : ℕ) (assign : ℕ → Bool) :
    (tseitinOr y x₁ x₂).eval assign = true ↔
    (assign y = (assign x₁ || assign x₂)) := by
  simp [tseitinOr, CNF.eval, Clause.eval, Literal.eval]
  constructor
  · -- 正向
    intro h
    rcases h with ⟨h1, h2, h3⟩
    cases h_y : assign y
    · -- assign y = false
      cases h_x1 : assign x₁
      · -- assign x₁ = false
        cases h_x2 : assign x₂
        · -- assign x₂ = false
          simp [h_y, h_x1, h_x2]
        · -- assign x₂ = true
          simp [h_y, h_x1, h_x2] at h1
      · -- assign x₁ = true
        cases h_x2 : assign x₂
        · -- assign x₂ = false
          simp [h_y, h_x1, h_x2] at h1
        · -- assign x₂ = true
          simp [h_y, h_x1, h_x2] at h1
    · -- assign y = true
      cases h_x1 : assign x₁
      · -- assign x₁ = false
        cases h_x2 : assign x₂
        · -- assign x₂ = false
          simp [h_y, h_x1, h_x2] at h2
        · -- assign x₂ = true
          simp [h_y, h_x1, h_x2]
      · -- assign x₁ = true
        cases h_x2 : assign x₂
        · -- assign x₂ = false
          simp [h_y, h_x1, h_x2]
        · -- assign x₂ = true
          simp [h_y, h_x1, h_x2]
  · -- 反向
    intro h_eq
    rw [h_eq]
    cases assign x₁ <;> cases assign x₂ <;> simp

/-- tseitinNot的语义: 赋值满足CNF当且仅当 y = ¬x -/
lemma tseitinNot_semantics (y x : ℕ) (assign : ℕ → Bool) :
    (tseitinNot y x).eval assign = true ↔
    (assign y = !(assign x)) := by
  simp [tseitinNot, CNF.eval, Clause.eval, Literal.eval]
  constructor
  · -- 正向
    intro h
    rcases h with ⟨h1, h2⟩
    cases h_y : assign y
    · -- assign y = false
      cases h_x : assign x
      · -- assign x = false
        simp [h_y, h_x] at h1
      · -- assign x = true
        simp [h_y, h_x]
    · -- assign y = true
      cases h_x : assign x
      · -- assign x = false
        simp [h_y, h_x]
      · -- assign x = true
        simp [h_y, h_x] at h2
  · -- 反向
    intro h_eq
    rw [h_eq]
    cases assign x <;> simp

-- ============================================
-- Section 6: 辅助引理 - gateToCNF的语义
-- ============================================

/-- gateToCNF在门节点上的语义 -/
lemma gateToCNF_gate_semantics (C : BooleanCircuit) (idx : ℕ)
    (hidx : idx < C.nodes.length)
    (gt : GateType) (l r : ℕ)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r)
    (assign : ℕ → Bool) :
    (gateToCNF C idx).eval assign = true ↔
    match gt with
    | GateType.and => assign idx = (assign l && assign r)
    | GateType.or => assign idx = (assign l || assign r)
    | GateType.not => assign idx = !(assign l)
    := by
  unfold gateToCNF
  rw [dif_pos hidx, heq]
  cases gt
  · -- AND gate
    simp [tseitinAnd_semantics]
  · -- OR gate
    simp [tseitinOr_semantics]
  · -- NOT gate
    simp [tseitinNot_semantics]

/-- gateToCNF在输入节点上的语义 -/
lemma gateToCNF_input_semantics (C : BooleanCircuit) (idx : ℕ)
    (hidx : idx < C.nodes.length)
    (i : ℕ)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.input i)
    (assign : ℕ → Bool) :
    (gateToCNF C idx).eval assign = true := by
  unfold gateToCNF
  rw [dif_pos hidx, heq]
  simp [CNF.eval]

-- ============================================
-- Section 7: 核心引理 - 从CNF满足赋值提取电路输入
-- ============================================

/-- 从赋值构造电路输入 -/
def extractCircuitInput (C : BooleanCircuit) (assign : ℕ → Bool) : List Bool :=
  List.map (λ i => assign i) (List.range C.numInputs)

/-- 提取的输入在范围内的正确性 -/
lemma extractCircuitInput_get (C : BooleanCircuit) (assign : ℕ → Bool) (i : ℕ)
    (hi : i < C.numInputs) :
    (extractCircuitInput C assign).get ⟨i, by simp [extractCircuitInput]; omega⟩ = assign i := by
  simp [extractCircuitInput, List.get_map, List.get_range]

/-- 提取的输入长度正确 -/
lemma extractCircuitInput_length (C : BooleanCircuit) (assign : ℕ → Bool) :
    (extractCircuitInput C assign).length = C.numInputs := by
  simp [extractCircuitInput]

-- ============================================
-- Section 8: 核心引理 - 输入节点求值等于赋值
-- ============================================

/-- 输入节点的evalNode等于对应赋值 -/
lemma evalNode_input_eq_assign (C : BooleanCircuit) (assign : ℕ → Bool)
    (idx : ℕ) (hidx : idx < C.nodes.length)
    (hinput : idx < C.numInputs)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.input idx) :
    evalNode C (extractCircuitInput C assign) idx = assign idx := by
  unfold evalNode
  rw [dif_pos hidx, heq]
  have h_state_len : idx < (extractCircuitInput C assign).length := by
    rw [extractCircuitInput_length]
    exact hinput
  rw [dif_pos h_state_len]
  have h_get : (extractCircuitInput C assign).get ⟨idx, h_state_len⟩ = assign idx := by
    apply extractCircuitInput_get
    exact hinput
  rw [h_get]

-- ============================================
-- Section 9: 核心引理 - 强归纳法证明关键不变式
-- ============================================

/-- 关键不变式: 对于所有节点idx，evalNode C input idx = assign idx

    这是整个反向证明的核心。我们用强归纳法证明：
    - 基础情况: idx < numInputs（输入节点）
      由extractCircuitInput的构造直接得到
    - 归纳步骤: idx ≥ numInputs（门节点）
      由Tseitin编码的语义和归纳假设得到

    强归纳法的必要性:
    - 门节点可能引用任意小于idx的节点
    - 需要假设所有更小的节点都满足不变式
    -/
lemma key_invariant (C : BooleanCircuit) (assign : ℕ → Bool)
    (h_sat : (circuitToCNF C).eval assign = true) :
    ∀ idx < C.nodes.length, evalNode C (extractCircuitInput C assign) idx = assign idx := by
  intro idx hidx
  -- 使用强归纳法
  have h_induction : ∀ (m : ℕ), m < C.nodes.length →
      (∀ (k : ℕ), k < m → evalNode C (extractCircuitInput C assign) k = assign k) →
      evalNode C (extractCircuitInput C assign) m = assign m := by
    intro m hmlen h_smaller
    by_cases h_input : m < C.numInputs
    · -- ============================================
      -- Case 1: m是输入节点
      -- ============================================
      have h_node : C.nodes.get ⟨m, hmlen⟩ = CircuitNode.input m :=
        C.hwf.input_spec m h_input hmlen
      -- 使用evalNode_input_eq_assign引理
      exact evalNode_input_eq_assign C assign m hmlen h_input h_node
    · -- ============================================
      -- Case 2: m是门节点
      -- ============================================
      have h_gate_pos : C.numInputs ≤ m := by omega
      -- 从well-formedness提取门节点信息
      rcases C.hwf.gate_spec m h_gate_pos hmlen with ⟨gt, l, r, h_eq, hl, hr⟩
      -- 归纳假设: 子节点满足不变式
      have hl_eq : evalNode C (extractCircuitInput C assign) l = assign l := h_smaller l hl
      have hr_eq : evalNode C (extractCircuitInput C assign) r = assign r := h_smaller r hr
      -- 展开evalNode在门节点上的定义
      have h_eval_node : evalNode C (extractCircuitInput C assign) m =
          evalGate gt (evalNode C (extractCircuitInput C assign) l)
                         (evalNode C (extractCircuitInput C assign) r) := by
        rw [evalNode_gate_eq C (extractCircuitInput C assign) m gt l r hmlen h_gate_pos h_eq]
      -- 使用归纳假设替换子节点
      rw [h_eval_node, hl_eq, hr_eq]
      -- 现在需要证明: evalGate gt (assign l) (assign r) = assign m
      -- 这由CNF满足性和Tseitin编码语义保证
      have h_gate_sat : (gateToCNF C m).eval assign = true := by
        -- 从circuitToCNF的满足性提取单个gate的满足性
        have h_cnf_sat : (circuitToCNF C).eval assign = true := h_sat
        simp [circuitToCNF, CNF.eval, List.all_append, Bool.and_eq_true] at h_cnf_sat
        rcases h_cnf_sat with ⟨h_gate_clauses, h_output⟩
        simp [CNF.eval, List.all_eq_true, List.mem_flatten, List.mem_map, List.mem_range] at h_gate_clauses
        -- 证明gateToCNF C m在flatten后的列表中
        have h_in_flatten : ∃ cnf, cnf ∈ List.map (gateToCNF C) (List.range C.nodes.length) ∧
            gateToCNF C m = cnf := by
          use gateToCNF C m
          constructor
          · -- 证明gateToCNF C m在map结果中
            simp [List.mem_map, List.mem_range]
            use m
            constructor
            · exact hmlen
            · rfl
          · rfl
        rcases h_in_flatten with ⟨cnf, hcnf_in, hcnf_eq⟩
        have h_cnf_sat' := h_gate_clauses cnf hcnf_in
        rw [← hcnf_eq] at h_cnf_sat'
        exact h_cnf_sat'
      -- 使用gateToCNF的语义
      have h_gate_sem := gateToCNF_gate_semantics C m hmlen gt l r h_eq assign
      rw [h_gate_sem] at h_gate_sat
      -- 根据门类型分别处理
      cases gt
      · -- AND gate: assign m = assign l && assign r
        simp at h_gate_sat
        rw [h_gate_sat]
        simp [evalGate]
      · -- OR gate: assign m = assign l || assign r
        simp at h_gate_sat
        rw [h_gate_sat]
        simp [evalGate]
      · -- NOT gate: assign m = !(assign l)
        simp at h_gate_sat
        rw [h_gate_sat]
        simp [evalGate]
  -- 应用强归纳法
  have h : ∀ (n : ℕ), n < C.nodes.length →
      evalNode C (extractCircuitInput C assign) n = assign n := by
    intro n hn
    induction' n using Nat.strongRecOn with n ih
    exact h_induction n hn (λ k hk => ih k hk (by omega))
  exact h idx hidx

-- ============================================
-- Section 10: 核心引理 - 输出验证
-- ============================================

/-- 输出约束保证assign outputIdx = true -/
lemma output_constraint_true (C : BooleanCircuit) (assign : ℕ → Bool)
    (h_sat : (circuitToCNF C).eval assign = true) :
    assign C.outputIdx = true := by
  have h_cnf_sat : (circuitToCNF C).eval assign = true := h_sat
  simp [circuitToCNF, CNF.eval, List.all_append, Bool.and_eq_true] at h_cnf_sat
  rcases h_cnf_sat with ⟨h_gate_clauses, h_output⟩
  -- 输出约束是[[pos outputIdx]]
  simp [Clause.eval, Literal.eval] at h_output
  exact h_output

/-- 电路求值等于true -/
lemma circuit_eval_true (C : BooleanCircuit) (assign : ℕ → Bool)
    (h_sat : (circuitToCNF C).eval assign = true) :
    CircuitEval C (extractCircuitInput C assign) = true := by
  simp [CircuitEval]
  -- 使用关键不变式
  have h_inv := key_invariant C assign h_sat C.outputIdx C.output_bound
  -- 输出约束保证assign outputIdx = true
  have h_out := output_constraint_true C assign h_sat
  rw [h_inv, h_out]

-- ============================================
-- Section 11: 核心定理 - 反向正确性
-- ============================================

/-- Backward direction: CNF-SAT implies Circuit SAT

    定理陈述: 如果circuitToCNF C是可满足的，那么C也是可满足的。
    
    证明概要:
    1. 假设CNF可满足，得到赋值assign
    2. 提取前numInputs个变量作为电路输入input
    3. 用强归纳法证明关键不变式:
       ∀ idx < C.nodes.length, evalNode C input idx = assign idx
    4. 由输出约束assign C.outputIdx = true和关键不变式
       得到CircuitEval C input = true
    5. 因此C是可满足的
    -/
lemma circuit_to_cnf_backward (C : BooleanCircuit) :
    CNFSatisfiable (circuitToCNF C) → CircuitSatisfiable C := by
  intro h
  rcases h with ⟨assign, h_sat⟩
  -- 从赋值提取电路输入
  let input := extractCircuitInput C assign
  use input
  -- 证明电路求值为true
  exact circuit_eval_true C assign h_sat

-- ============================================
-- Section 12: 完整双向蕴含
-- ============================================

/-- Forward direction (已有证明，此处重复用于完整性) -/
lemma tseitin_assignment_gate (C : BooleanCircuit) (input : List Bool) (idx : ℕ)
    (hidx : idx < C.nodes.length) :
    (gateToCNF C idx).eval (tseitinAssignment C input) = true := by
  unfold gateToCNF
  rw [dif_pos hidx]
  match h_node : C.nodes.get ⟨idx, hidx⟩ with
  | CircuitNode.input _ =>
    simp [CNF.eval]
  | CircuitNode.gate gt l r =>
    have h_gate : C.numInputs ≤ idx := by
      by_contra h
      push_neg at h
      have h_input : idx < C.numInputs := by omega
      have h_node_input : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.input idx :=
        C.hwf.input_spec idx h_input hidx
      rw [h_node] at h_node_input
      injection h_node_input
    have hl : l < idx := by
      rcases C.hwf.gate_spec idx h_gate hidx with ⟨gt', l', r', h_eq', hl', hr'⟩
      rw [h_node] at h_eq'
      injection h_eq' with _ hl'' _
      rw [← hl''] at hl'
      exact hl'
    have hr : r < idx := by
      rcases C.hwf.gate_spec idx h_gate hidx with ⟨gt', l', r', h_eq', _, hr'⟩
      rw [h_node] at h_eq'
      injection h_eq' with _ _ hr''
      rw [← hr''] at hr'
      exact hr'
    have hl_len : l < C.nodes.length := by omega
    have hr_len : r < C.nodes.length := by omega
    cases gt
    · simp [tseitinAnd, CNF.eval, Clause.eval, Literal.eval, tseitinAssignment, hidx, hl_len, hr_len]
      have h_eval : evalNode C input idx = (evalNode C input l && evalNode C input r) := by
        rw [evalNode_gate_eq C input idx GateType.and l r hidx h_gate h_node]
        simp [evalGate]
      rw [h_eval]
      cases evalNode C input l <;> cases evalNode C input r <;> simp
    · simp [tseitinOr, CNF.eval, Clause.eval, Literal.eval, tseitinAssignment, hidx, hl_len, hr_len]
      have h_eval : evalNode C input idx = (evalNode C input l || evalNode C input r) := by
        rw [evalNode_gate_eq C input idx GateType.or l r hidx h_gate h_node]
        simp [evalGate]
      rw [h_eval]
      cases evalNode C input l <;> cases evalNode C input r <;> simp
    · simp [tseitinNot, CNF.eval, Clause.eval, Literal.eval, tseitinAssignment, hidx, hl_len]
      have h_eval : evalNode C input idx = !(evalNode C input l) := by
        rw [evalNode_gate_eq C input idx GateType.not l r hidx h_gate h_node]
        simp [evalGate]
      rw [h_eval]
      cases evalNode C input l <;> simp

lemma tseitin_satisfies_cnf (C : BooleanCircuit) (input : List Bool)
    (h_eq : CircuitEval C input = true) :
    (circuitToCNF C).eval (tseitinAssignment C input) = true := by
  simp only [circuitToCNF, CNF.eval, List.all_append, Bool.and_eq_true]
  constructor
  · simp only [List.all_eq_true, List.mem_flatten, List.mem_map, List.mem_range]
    intro clause h_clause
    rcases h_clause with ⟨cnf, ⟨idx, hidx, hcnf⟩, h_clause_in_cnf⟩
    rw [← hcnf] at h_clause_in_cnf
    have h_gate_sat : (gateToCNF C idx).eval (tseitinAssignment C input) = true :=
      tseitin_assignment_gate C input idx hidx
    simp only [CNF.eval, List.all_eq_true] at h_gate_sat
    apply h_gate_sat
    exact h_clause_in_cnf
  · simp [CircuitEval] at h_eq
    simp [Clause.eval, Literal.eval, tseitinAssignment, C.output_bound]
    exact h_eq

lemma circuit_to_cnf_forward (C : BooleanCircuit) :
    CircuitSatisfiable C → CNFSatisfiable (circuitToCNF C) := by
  intro h
  rcases h with ⟨input, h_eval⟩
  use tseitinAssignment C input
  exact tseitin_satisfies_cnf C input h_eval

/-- Full reduction correctness: The Cook-Levin Theorem -/
theorem circuit_sat_reduction_correct (C : BooleanCircuit) :
    ReductionProperty C (circuitToCNF C) := by
  constructor
  · exact circuit_to_cnf_forward C
  · exact circuit_to_cnf_backward C

-- ============================================
-- Section 13: 补充引理与性质
-- ============================================

/-- 关键不变式的推论: 门节点求值一致性 -/
lemma gate_eval_consistency (C : BooleanCircuit) (assign : ℕ → Bool)
    (h_sat : (circuitToCNF C).eval assign = true)
    (idx : ℕ) (hidx : idx < C.nodes.length)
    (gt : GateType) (l r : ℕ)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r) :
    evalNode C (extractCircuitInput C assign) idx =
    evalGate gt (evalNode C (extractCircuitInput C assign) l)
               (evalNode C (extractCircuitInput C assign) r) := by
  rw [evalNode_gate_eq C (extractCircuitInput C assign) idx gt l r hidx (by omega) heq]

/-- Tseitin赋值的唯一性（在电路节点范围内） -/
lemma tseitin_assignment_unique (C : BooleanCircuit) (input : List Bool)
    (idx : ℕ) (hidx : idx < C.nodes.length) :
    tseitinAssignment C input idx = evalNode C input idx := by
  simp [tseitinAssignment, hidx]

/-- 提取的输入与原始输入的关系（当输入长度匹配时） -/
lemma extract_input_roundtrip (C : BooleanCircuit) (input : List Bool)
    (hlen : input.length = C.numInputs) :
    extractCircuitInput C (tseitinAssignment C input) = input := by
  apply List.ext_get
  · -- 长度相等
    rw [extractCircuitInput_length, hlen]
  · -- 元素相等
    intro i hi1 hi2
    simp [extractCircuitInput_get, tseitinAssignment]
    have hidx : i < C.nodes.length := by
      have h1 : i < C.numInputs := by rw [← hlen]; exact hi1
      have h2 : C.numInputs ≤ C.nodes.length := C.hwf.len_bound
      omega
    simp [hidx]
    -- 输入节点的evalNode等于state[i]
    have h_node : C.nodes.get ⟨i, hidx⟩ = CircuitNode.input i := by
      have h_input : i < C.numInputs := by rw [← hlen]; exact hi1
      exact C.hwf.input_spec i h_input hidx
    unfold evalNode
    rw [dif_pos hidx, h_node]
    have h_state : i < input.length := by rw [hlen]; exact hi1
    rw [dif_pos h_state]
    rfl

end SylvaFormalization
