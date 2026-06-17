import os
import shutil

# 1. Create SylvaFormalization directory
os.makedirs('SylvaFormalization', exist_ok=True)

# 2. Fix Basic.lean and move to SylvaFormalization/Basic.lean
with open('Basic.lean', 'r', encoding='utf-8') as f:
    basic = f.read()
# Fix literal backslash-n
basic = basic.replace('\\n', '\n')

with open('SylvaFormalization/Basic.lean', 'w', encoding='utf-8') as f:
    f.write(basic)
print('Fixed and moved Basic.lean')

# 3. Fix NavierStokes.lean and add Phi namespace
with open('NavierStokes.lean', 'r', encoding='utf-8') as f:
    ns = f.read()
ns = ns.replace('\\n', '\n')

# Add Phi namespace after imports, before namespace Sylva
phi_def = """/-- Sylva Phi namespace: critical value framework for bootstrap analysis -/
namespace Phi
  /-- Critical value Φ_c = 137 × φ³
      Derived from Sylva's bootstrap framework, connecting to golden ratio properties.
      Used in the Navier-Stokes energy-debt analogy. -/
  noncomputable def Phi_c : ℝ := 137 * ((1 + Real.sqrt 5) / 2) ^ 3
end Phi

"""

ns = ns.replace('namespace Sylva\nnamespace NavierStokes', 
                  phi_def + 'namespace Sylva\nnamespace NavierStokes')

with open('SylvaFormalization/NavierStokes.lean', 'w', encoding='utf-8') as f:
    f.write(ns)
print('Fixed and moved NavierStokes.lean')

# 4. Verify
with open('SylvaFormalization/NavierStokes.lean', 'r', encoding='utf-8') as f:
    ns_check = f.read()
print('sorry count:', ns_check.count('sorry'))
print('axiom count:', ns_check.count('axiom'))
print('Contains Phi_c:', 'Phi_c' in ns_check)
print('Contains Phi namespace:', 'namespace Phi' in ns_check)
