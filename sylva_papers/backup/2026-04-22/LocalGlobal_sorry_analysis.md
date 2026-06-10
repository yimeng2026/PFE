# LocalGlobal.lean Sorry Fix Analysis

## Summary of 6 Sorries

### 1. cookLevinLocalGlobal.descent_restriction (line 272)
**Context**: The `restriction` function returns an empty CNF `[]`, losing the original CNF information. The `descent_restriction` field requires proving that `restriction (descent d hc) = d`, which is impossible because:
- `descent` creates an assignment from the circuit
- `restriction` always returns `⟨Classical.choose g.prop, []⟩` (empty CNF)
- The CNF information is lost

**Analysis**: This is a fundamental design issue - the restriction function doesn't actually reconstruct the original local data.

### 2. bsdLocalGlobal.descent_restriction (line 365)
**Context**: The `descent` function returns a placeholder `(0, 0)`, not the actual L-function values. The `restriction` extracts Euler factors. These don't compose back to the original.

**Analysis**: BSD requires deep L-function theory - this is a conceptual framework stub.

### 3. hodgeLocalGlobal.descent_restriction (line 448)
**Context**: The `descent` returns zero cycle `⟨0, AlgebraicCycle.zero⟩`. The `restriction` extracts differential forms. These don't compose.

**Analysis**: Hodge conjecture is unsolved - this is intentionally a stub.

### 4. composeLocalGlobal.descent hc2 (line 539)
**Context**: Need to prove `P2.compatibility (cast h.symm g1)` where `g1 = P1.descent d hc`. 

**Analysis**: This requires that the output of P1's descent satisfies P2's compatibility condition. This is not automatically true and needs an assumption.

### 5. composeLocalGlobal.compatibility_restriction (line 551)
**Context**: Need to prove that after restricting through the composite, the result satisfies P1's compatibility.

**Analysis**: This chains P2's `compatibility_restriction` with the cast operation.

### 6. composeLocalGlobal.descent_restriction (line 562)
**Context**: Need to prove the descent-restriction identity for the composite.

**Analysis**: This is complex because:
- hc2 is defined in a let-binding, making it hard to unfold
- The proof needs to use P2's `descent_restriction` but hc2 is not the "right" proof term

## Fix Strategy

1. **For Cook-Levin**: Add a proper `restriction` that preserves CNF, or add an extra hypothesis that the assignment uniquely determines the CNF.

2. **For BSD/Hodge**: These are deep mathematical open problems. Keep as conceptual stubs with proper documentation.

3. **For composeLocalGlobal**: Refactor to take the compatibility condition as an explicit argument rather than a let-binding, allowing the proof to reference it.
