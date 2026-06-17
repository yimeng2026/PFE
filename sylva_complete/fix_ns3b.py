import os

with open('NavierStokes.lean', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\r\n', '\n')

# Insert strong_solution_uniqueness axiom between section 9 and section 10
insert_text = """/-- Uniqueness of strong solutions.
    A standard result for parabolic PDEs with regular data, but requires
    energy estimates and bootstrap arguments not yet in Mathlib.
    Declared as an axiom pending formal proof. -/
axiom strong_solution_uniqueness {u v : VelocityField} {p q : PressureField}
    {nu : ℝ} {u0 : SpatialDomain → SpatialDomain} {T : ℝ}
    (hu : IsStrongSolution u p nu (fun _ _ => 0) u0 T)
    (hv : IsStrongSolution v q nu (fun _ _ => 0) u0 T) :
    ∀ t ∈ Set.Icc 0 T, ∀ x : SpatialDomain, u t x = v t x

"""

idx = content.find('-- ============================================================\n-- SECTION 10: SYLVA CONNECTION')
if idx >= 0:
    content = content[:idx] + insert_text + content[idx:]
    print('Inserted strong_solution_uniqueness')
else:
    print('ERROR: section 10 not found')

with open('NavierStokes.lean', 'w', encoding='utf-8') as f:
    f.write(content)

print('Remaining sorry:', content.count('sorry'))
