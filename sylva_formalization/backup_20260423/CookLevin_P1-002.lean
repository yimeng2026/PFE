/-
================================================================================
P1-002: evalNode_gate_eq 引理证明
================================================================================

目标: 证明 CookLevin 模块中 evalNode 函数的 gate 等价性引理

引理陈述:
  lemma evalNode_gate_eq (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
      (gt : GateType) (l r : ℕ)
      (hidx : idx < C.nodes.length)
      (hgate : C.numInputs ≤ idx)
      (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r) :
      evalNode C state idx = evalGate gt (evalNode C state l) (evalNode C state r)

核心思路:
  1. evalNode 使用 well-founded recursion (按 idx 递减)
  2. 当 C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r 时,
     evalNode 的定义直接展开为 evalGate gt (evalNode C state l) (evalNode C state r)
  3. 证明的关键在于正确处理 WellFounded.fix 的展开
  4. 使用 WellFounded.fix_eq 引理来展开递归定义

证明策略:
  - 使用 unfold evalNode 展开定义
  - 使用 dif_pos hidx 处理条件分支 (idx < C.nodes.length 为真)
  - 使用 match 的目标替换 (heq) 来处理节点类型匹配
  - 使用 WellFounded.fix_eq 来展开 well-founded 递归
  - 利用电路的良构性保证 l < idx 和 r < idx,从而递归终止
================================================================================
-/

import Mathlib
import SylvaFormalization.Basic

namespace SylvaFormalization

-- ============================================
-- Section 1: Boolean Circuits (从 CookLevin_fixed.lean 复制核心定义)
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

/-- Evaluate a gate -/
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

-- ============================================
-- Section 2: evalNode_gate_eq 引理证明 (P1-002)
-- ============================================

/--
P1-002 核心引理: evalNode 在 gate 节点处的展开等价性

当 idx 指向一个 gate 节点时,evalNode 的求值结果等价于对该 gate
的左右子节点递归求值后再应用 evalGate。

这是整个 Cook-Levin 证明的基础引理之一,被 tseitin_assignment_gate 等
后续引理所依赖。
-/
lemma evalNode_gate_eq (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (gt : GateType) (l r : ℕ)
    (hidx : idx < C.nodes.length)
    (hgate : C.numInputs ≤ idx)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r) :
    evalNode C state idx = evalGate gt (evalNode C state l) (evalNode C state r) := by

  -- ============================================================
  -- Step 1: 展开 evalNode 的定义
  -- ============================================================
  -- evalNode 的定义结构:
  --   if h : idx < C.nodes.length then
  --     match heq : C.nodes.get ⟨idx, h⟩ with
  --     | CircuitNode.input i => ...
  --     | CircuitNode.gate gt l r => evalGate gt (evalNode C state l) (evalNode C state r)
  --   else false
  --
  -- 由于我们有 hidx : idx < C.nodes.length,条件分支走 then 分支
  -- 由于我们有 heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r,
  -- match 走 gate 分支

  unfold evalNode

  -- ============================================================
  -- Step 2: 处理条件分支 (idx < C.nodes.length)
  -- ============================================================
  -- 使用 dif_pos 将 if h : idx < C.nodes.length then ... else ...
  -- 替换为 then 分支的内容,并添加 hidx 作为假设

  simp only [dif_pos hidx]

  -- ============================================================
  -- Step 3: 处理 match 表达式
  -- ============================================================
  -- 此时目标中应该有一个 match 表达式:
  --   match heq : C.nodes.get ⟨idx, hidx⟩ with
  --   | CircuitNode.input i => ...
  --   | CircuitNode.gate gt l r => evalGate gt (evalNode C state l) (evalNode C state r)
  --
  -- 由于我们已经知道 heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r,
  -- match 会匹配到 gate 分支
  --
  -- 使用 split 来展开 match,然后选择正确的分支

  split
  · -- 这个分支对应 match 的 input 情况
    -- 但我们有 heq 说这是一个 gate,所以这里应该产生矛盾
    rename_i i h_input
    -- h_input : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.input i
    -- heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r
    -- 这两个等式矛盾
    rw [heq] at h_input
    injection h_input

  · -- 这个分支对应 match 的 gate 情况
    -- 这正是我们想要的情况
    rename_i gt' l' r' h_gate
    -- h_gate : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt' l' r'
    -- 与 heq 结合,得到 gt = gt', l = l', r = r'
    rw [heq] at h_gate
    injection h_gate with h_gt h_l h_r
    -- 现在我们有:
    -- h_gt : gt = gt'
    -- h_l : l = l'
    -- h_r : r = r'
    -- 代入这些等式即可完成证明
    simp [h_gt, h_l, h_r]

-- ============================================
-- Section 3: 辅助引理 - 良构性保证子节点索引更小
-- ============================================

/--
从电路良构性提取: gate 节点的左子节点索引小于当前节点索引
-/
lemma gate_left_lt (C : BooleanCircuit) (idx : ℕ)
    (hidx : idx < C.nodes.length)
    (hgate : C.numInputs ≤ idx)
    (gt : GateType) (l r : ℕ)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r) :
    l < idx := by
  rcases C.hwf.gate_spec idx hgate hidx with ⟨gt', l', r', h_eq', hl', hr'⟩
  rw [heq] at h_eq'
  injection h_eq' with h_gt h_l h_r
  rw [← h_l] at hl'
  exact hl'

/--
从电路良构性提取: gate 节点的右子节点索引小于当前节点索引
-/
lemma gate_right_lt (C : BooleanCircuit) (idx : ℕ)
    (hidx : idx < C.nodes.length)
    (hgate : C.numInputs ≤ idx)
    (gt : GateType) (l r : ℕ)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r) :
    r < idx := by
  rcases C.hwf.gate_spec idx hgate hidx with ⟨gt', l', r', h_eq', hl', hr'⟩
  rw [heq] at h_eq'
  injection h_eq' with h_gt h_l h_r
  rw [← h_r] at hr'
  exact hr'

-- ============================================
-- Section 4: evalNode 终止性证明 (P1-001 相关)
-- ============================================

/--
P1-001: evalNode 的 well-founded 递归终止性证明

这个引理证明 evalNode 中递归调用 evalNode C state l 和
evalNode C state r 时,l 和 r 都小于 idx,从而保证递归终止。

注意: 这个证明需要作为 decreasing_by 块的替代方案,或者
在定义 evalNode 时直接使用。
-/
lemma evalNode_termination (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (hidx : idx < C.nodes.length)
    (hgate : C.numInputs ≤ idx)
    (gt : GateType) (l r : ℕ)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r) :
    l < idx ∧ r < idx := by
  constructor
  · exact gate_left_lt C idx hidx hgate gt l r heq
  · exact gate_right_lt C idx hidx hgate gt l r heq

-- ============================================
-- Section 5: evalNode 在 input 节点处的展开
-- ============================================

/--
evalNode 在 input 节点处的展开:
当 idx 指向一个 input 节点时,evalNode 返回对应的 state 值
-/
lemma evalNode_input_eq (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (i : ℕ)
    (hidx : idx < C.nodes.length)
    (hinput : idx < C.numInputs)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.input i) :
    evalNode C state idx = if h' : i < state.length then state.get ⟨i, h'⟩ else false := by

  unfold evalNode
  simp only [dif_pos hidx]

  split
  · -- input 分支
    rename_i i' h_input
    rw [heq] at h_input
    injection h_input with h_i
    simp [h_i]

  · -- gate 分支,应该产生矛盾
    rename_i gt l r h_gate
    rw [heq] at h_gate
    injection h_gate

-- ============================================
-- Section 6: evalNode 在越界情况下的行为
-- ============================================

/--
evalNode 在 idx ≥ C.nodes.length 时返回 false
-/
lemma evalNode_oob_eq_false (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (hidx : idx ≥ C.nodes.length) :
    evalNode C state idx = false := by
  unfold evalNode
  simp only [dif_neg (by omega)]

-- ============================================
-- Section 7: evalNode_gate_eq 的变体形式
-- ============================================

/--
evalNode_gate_eq 的 AND 门特化版本
-/
lemma evalNode_and_eq (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (l r : ℕ)
    (hidx : idx < C.nodes.length)
    (hgate : C.numInputs ≤ idx)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate GateType.and l r) :
    evalNode C state idx = (evalNode C state l && evalNode C state r) := by
  rw [evalNode_gate_eq C state idx GateType.and l r hidx hgate heq]
  simp [evalGate]

/--
evalNode_gate_eq 的 OR 门特化版本
-/
lemma evalNode_or_eq (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (l r : ℕ)
    (hidx : idx < C.nodes.length)
    (hgate : C.numInputs ≤ idx)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate GateType.or l r) :
    evalNode C state idx = (evalNode C state l || evalNode C state r) := by
  rw [evalNode_gate_eq C state idx GateType.or l r hidx hgate heq]
  simp [evalGate]

/--
evalNode_gate_eq 的 NOT 门特化版本
注意: NOT 门只使用左子节点,右子节点被忽略
-/
lemma evalNode_not_eq (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (l r : ℕ)
    (hidx : idx < C.nodes.length)
    (hgate : C.numInputs ≤ idx)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate GateType.not l r) :
    evalNode C state idx = !(evalNode C state l) := by
  rw [evalNode_gate_eq C state idx GateType.not l r hidx hgate heq]
  simp [evalGate]

-- ============================================
-- Section 8: 强归纳法框架 (用于后续证明)
-- ============================================

/--
基于节点索引的强归纳原理

对于电路中的每个节点,如果对于所有索引小于 idx 的节点性质 P 成立,
那么 P 对 idx 也成立,则 P 对所有有效节点索引成立。
-/
theorem evalNode_strong_induction (C : BooleanCircuit) (state : List Bool)
    (P : ℕ → Prop)
    (h_base : ∀ i < C.numInputs, P i)
    (h_step : ∀ idx, C.numInputs ≤ idx → idx < C.nodes.length →
      (∀ l r gt, C.nodes.get ⟨idx, by assumption⟩ = CircuitNode.gate gt l r →
        l < idx → r < idx → P l → P r → P idx) →
      P idx) :
    ∀ idx < C.nodes.length, P idx := by

  intro idx hidx
  -- 使用 Nat.strongRecOn 进行强归纳
  induction' idx using Nat.strongRecOn with idx ih
  by_cases h_input : idx < C.numInputs
  · -- 基本情况: idx 是输入节点
    exact h_base idx h_input
  · -- 归纳情况: idx 是 gate 节点
    have h_gate_pos : C.numInputs ≤ idx := by omega
    rcases C.hwf.gate_spec idx h_gate_pos hidx with ⟨gt, l, r, h_eq, hl, hr⟩
    have h_pl : P l := ih l hl (by omega)
    have h_pr : P r := ih r hr (by omega)
    -- 这里需要构造 h_step 所需的参数
    -- 由于类型系统限制,这个框架需要进一步细化
    sorry

end SylvaFormalization
