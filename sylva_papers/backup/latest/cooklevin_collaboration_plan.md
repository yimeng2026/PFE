# CookLevin.lean - 5个 sorry 依赖分析与协作填充计划

## 📍 精确的 sorry 位置

| # | 行号 | 所在引理/定理 | 描述 |
|---|------|--------------|------|
| 1 | 125 | `evalNode_gate_eq` | 证明 evalNode 在门电路索引处等于 evalGate 应用 |
| 2 | 310 | `tseitin_satisfies_cnf` | 证明 Tseitin 赋值满足完整 CNF 编码 |
| 3 | 380 | `circuit_to_cnf_backward.h_induction` | 从 Tseitin 约束中提取门语义 |
| 4 | 382 | `circuit_to_cnf_backward.h_key_invariant` | 应用强归纳原理 |
| 5 | 391 | `circuit_to_cnf_backward.h_output` | 证明输出约束为 true |

---

## 🔗 依赖关系图

```
┌─────────────────────────────────────────────────────────────────┐
│                        依赖层级 0 (基础)                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Sorry #1: evalNode_gate_eq                              │   │
│  │ 位置: 行 125                                             │   │
│  │ 难度: ⭐⭐⭐ (Well-founded recursion + dependent match)   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       依赖层级 1 (中间)                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Sorry #2: tseitin_satisfies_cnf                         │   │
│  │ 位置: 行 310                                             │   │
│  │ 依赖: tseitin_assignment_gate (已证) → 用 evalNode_gate_eq│   │
│  │ 难度: ⭐⭐ (List induction)                               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       依赖层级 2 (组合)                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Sorry #3-5: circuit_to_cnf_backward                     │   │
│  │ 位置: 行 380, 382, 391                                   │   │
│  │ 依赖: evalNode_gate_eq + h_sat (CNF满足性)               │   │
│  │ 内部依赖:                                                │   │
│  │   #3 (归纳步骤) ──→ #4 (强归纳应用) ──→ #5 (输出约束)     │   │
│  │ 难度: ⭐⭐⭐⭐ (复杂的双向归约证明)                         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔍 详细依赖分析

### 1. `evalNode_gate_eq` (Sorry #1)

**上下文:**
```lean
lemma evalNode_gate_eq (C : BooleanCircuit) (state : List Bool) (idx : ℕ)
    (gt : GateType) (l r : ℕ)
    (hidx : idx < C.nodes.length)
    (hgate : C.numInputs ≤ idx)
    (heq : C.nodes.get ⟨idx, hidx⟩ = CircuitNode.gate gt l r) :
    evalNode C state idx = evalGate gt (evalNode C state l) (evalNode C state r)
```

**证明策略:**
- 展开 `evalNode` 定义 (使用 well-founded recursion)
- 利用 `hidx` 和 `hgate` 简化条件分支
- 处理 dependent pattern matching
- 使用 `heq` 确保门类型匹配

**依赖影响:**
- ✅ **被 `tseitin_assignment_gate` 使用** (行 256, 267, 276)
- ✅ **被 `circuit_to_cnf_backward` 使用** (行 373)

**结论:** 这是**最基础的引理**，必须先完成！

---

### 2. `tseitin_satisfies_cnf` (Sorry #2)

**上下文:**
```lean
lemma tseitin_satisfies_cnf (C : BooleanCircuit) (input : List Bool)
    (h_eq : CircuitEval C input = true) :
    (circuitToCNF C).eval (tseitinAssignment C input) = true
```

**证明策略:**
- 展开 `circuitToCNF` = gateClauses ++ outputConstraint
- 使用 `tseitin_assignment_gate` 证明每个门约束被满足
- 使用 `h_eq` 证明输出约束被满足
- 需要 `List.all` 和 `List.flatten` 相关的列表引理

**依赖关系:**
- 依赖 `tseitin_assignment_gate` (已完整证明，无 sorry)
- `tseitin_assignment_gate` 又依赖 `evalNode_gate_eq`

**结论:** 必须在 `evalNode_gate_eq` 完成后才能填充。

---

### 3. `circuit_to_cnf_backward` 内部的 3 个 sorry

**整体结构:**
```lean
lemma circuit_to_cnf_backward (C : BooleanCircuit) :
    CNFSatisfiable (circuitToCNF C) → CircuitSatisfiable C := by
  intro h
  rcases h with ⟨assign, h_sat⟩
  let input := List.map (λ i => assign i) (List.range C.numInputs)
  use input
  
  have h_key_invariant : ∀ idx < C.nodes.length, evalNode C input idx = assign idx := by
    have h_induction : ∀ (m : ℕ), ... → evalNode C input m = assign m := by
      ...
      sorry  -- #3: 门语义提取 (行 380)
    sorry      -- #4: 强归纳应用 (行 382)
  
  have h_output : CircuitEval C input = true := by
    ...
    sorry      -- #5: 输出约束 (行 391)
```

**内部依赖链:**

```
┌─────────────────────────────────────────────────────────┐
│ Sorry #3 (行 380): 归纳步骤中的门语义提取                   │
│                                                         │
│ 目标: 证明 assign m = evalGate gt (assign l) (assign r) │
│      从 CNF 满足性 h_sat 中提取门约束信息                 │
│                                                         │
│ 难点: 需要在 h_sat 中定位 gateToCNF C m 的约束            │
│      并证明它们强制门变量等于门求值结果                    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Sorry #4 (行 382): 强归纳应用                              │
│                                                         │
│ 目标: 使用强归纳原理证明 ∀ idx < len, invariant holds   │
│                                                         │
│ 依赖: 必须先完成 #3，因为归纳步骤需要它                    │
│  tactic: Nat.strongInduction 或手动构造                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Sorry #5 (行 391): 输出约束证明                            │
│                                                         │
│ 目标: 证明 assign C.outputIdx = true                     │
│      从 h_sat 和 outputConstraint 中提取                 │
│                                                         │
│ 依赖: 需要先完成 #4，因为需要用到 h_key_invariant        │
│       来连接 evalNode 和 assign                          │
└─────────────────────────────────────────────────────────┘
```

**外部依赖:**
- 使用 `evalNode_gate_eq` (行 373)
- 依赖 `h_sat` (CNF 满足性假设)

---

## 👥 3-Agent 协作计划

### Agent A: 基础引理专家
**任务:** Sorry #1 - `evalNode_gate_eq`

**输入:**
- 文件: CookLevin.lean (行 95-130)
- 目标: 完成 evalNode_gate_eq 的证明

**证明指导:**
```lean
lemma evalNode_gate_eq ... := by
  unfold evalNode
  rw [dif_pos hidx, dif_neg hgate]  -- idx >= numInputs, so gate branch
  -- 处理 dependent match on C.nodes.get ⟨idx, hidx⟩
  split
  · -- 矛盾情况: 输入节点
    exfalso
    -- 使用 heq 和 gate 假设的矛盾
  · -- gate 情况
    -- 使用 heq 匹配 gt, l, r
    -- well-foundedness 自动处理递归
    simp [evalGate]
    all_goals try { tauto } <|> { omega }
```

**预期产出:**
- 文件: `CookLevin_agentA.lean` 或 PR 到主文件
- 测试: `lake build` 通过

**时间估计:** 中等 (well-founded recursion 证明技巧)

---

### Agent B: 中间证明专家
**任务:** Sorry #2 - `tseitin_satisfies_cnf`

**输入:**
- 文件: CookLevin.lean (行 295-315)
- 前提: Agent A 完成 evalNode_gate_eq
- 可用引理: `tseitin_assignment_gate` (已证)

**证明指导:**
```lean
lemma tseitin_satisfies_cnf ... := by
  unfold circuitToCNF CNF.eval
  -- 分解为 gateClauses 和 outputConstraint
  constructor
  · -- 证明所有 gateClauses 被满足
    apply List.all_of_forall
    intro clause h_clause
    -- 使用 tseitin_assignment_gate
    simp [List.flatten, List.map] at h_clause
    -- 需要列表操作引理来定位特定门
    sorry -- 列表归纳部分
  · -- 证明 outputConstraint 被满足
    simp [h_eq, tseitinAssignment, CircuitEval]
    -- output 约束强制 outputIdx 为 true
```

**预期产出:**
- 文件: `CookLevin_agentB.lean` 或 PR
- 依赖: Agent A 的成果

**时间估计:** 中等偏易 (主要是列表操作)

---

### Agent C: 最终组合专家
**任务:** Sorry #3, #4, #5 - `circuit_to_cnf_backward`

**输入:**
- 文件: CookLevin.lean (行 345-395)
- 前提: Agent A 完成 evalNode_gate_eq
- 策略: 内部顺序填充 #3 → #4 → #5

**分阶段计划:**

**阶段 1 - Sorry #3 (门语义提取):**
```lean
-- 在 h_induction 的 inductive case 中
-- 目标: prove assign m = evalGate gt (assign l) (assign r)
-- 从 h_sat 中提取 gateToCNF C m 的满足性
have h_gate_cnf : (gateToCNF C m).eval assign = true := by
  -- 在 h_sat 中定位 gateToCNF 的约束
  simp [circuitToCNF, CNF.eval, List.all, List.flatten] at h_sat
  -- 使用 List.mem 和存在量词推理
  sorry

-- 展开 gateToCNF 和 tseitin 约束
rcases gt
· -- AND gate
  simp [gateToCNF, tseitinAnd, CNF.eval, Clause.eval] at h_gate_cnf
  -- 现在 h_gate_cnf 包含3个子句的真值
  -- 通过布尔逻辑推导 assign m = assign l && assign r
  sorry
```

**阶段 2 - Sorry #4 (强归纳应用):**
```lean
-- 使用 Nat.strongRecOn 或手动强归纳
exact Nat.strongRecOn (motive := λ m => m < C.nodes.length → evalNode C input m = assign m) 
  idx hidx h_induction
```

**阶段 3 - Sorry #5 (输出约束):**
```lean
have h_output_sat : (outputConstraint C).eval assign = true := by
  simp [circuitToCNF, CNF.eval, outputConstraint] at h_sat
  sorry

-- 结合 h_key_invariant 和 h_output_sat
simp [CircuitEval]
rw [h_key_invariant C.outputIdx C.output_bound]
-- 证明 assign C.outputIdx = true
```

**预期产出:**
- 文件: `CookLevin_agentC.lean` 或 PR
- 依赖: Agent A 的成果 (Agent B 可选，因为是独立方向)

**时间估计:** 困难 (最复杂的双向归约)

---

## 📋 执行顺序与协作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                        并行阶段 1                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Agent A: evalNode_gate_eq                                │   │
│  │ 优先级: 🔴 最高 (阻塞其他所有任务)                        │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        并行阶段 2                                │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐ │
│  │ Agent B:                │  │ Agent C Phase 1:             │ │
│  │ tseitin_satisfies_cnf   │  │ circuit_to_cnf_backward #3   │ │
│  │                         │  │ (门语义提取)                  │ │
│  │ 依赖: A                 │  │ 依赖: A                      │ │
│  └─────────────────────────┘  └──────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│                   ┌─────────────────────────┐                  │
│                   │ Agent C Phase 2:        │                  │
│                   │ #4 (强归纳应用)           │                  │
│                   │ 依赖: C Phase 1          │                  │
│                   └─────────────────────────┘                  │
│                              │                                  │
│                              ▼                                  │
│                   ┌─────────────────────────┐                  │
│                   │ Agent C Phase 3:        │                  │
│                   │ #5 (输出约束)             │                  │
│                   │ 依赖: C Phase 2          │                  │
│                   └─────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        整合阶段                                   │
│  - 合并所有 sorry 填充结果                                       │
│  - 验证 lake build SylvaFormalization.CookLevin 通过             │
│  - 生成最终报告                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 关键依赖总结

| 依赖方 | 被依赖方 | 关系类型 |
|--------|----------|----------|
| `tseitin_assignment_gate` (已证) | `evalNode_gate_eq` | 直接使用 (行 256, 267, 276) |
| `tseitin_satisfies_cnf` (#2) | `tseitin_assignment_gate` | 逻辑依赖 |
| `circuit_to_cnf_backward` #3 | `evalNode_gate_eq` | 直接使用 (行 373) |
| `circuit_to_cnf_backward` #4 | `circuit_to_cnf_backward` #3 | 内部顺序 |
| `circuit_to_cnf_backward` #5 | `circuit_to_cnf_backward` #4 | 内部顺序 |

**关键路径:** #1 → (并行 #2 和 #3) → #4 → #5

---

## 📝 Agent 通信协议

1. **Agent A 完成时:**
   - 提交 `evalNode_gate_eq` 的证明
   - 通知 Agent B 和 Agent C 可以开始

2. **Agent B 完成时:**
   - 提交 `tseitin_satisfies_cnf` 的证明
   - 这是独立成果，不阻塞其他任务

3. **Agent C 阶段报告:**
   - Phase 1 (#3) 完成后报告
   - Phase 2 (#4) 完成后报告
   - Phase 3 (#5) 完成后报告最终成果

4. **最终整合:**
   - 所有 Agent 的成果合并到 CookLevin.lean
   - 运行 `lake build SylvaFormalization.CookLevin` 验证
   - 生成 CookLevin_final.lean 和 CookLevin_final_report.md

---

*计划生成时间: 2026-04-15*
*目标: 完成 CookLevin 定理的形式化证明*
