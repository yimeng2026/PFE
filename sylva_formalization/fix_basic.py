import re

# Read the file
with open(r'C:\Users\一梦\.kimi_openclaw\workspace\sylva_formalization\SylvaFormalization\Basic.lean', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Type annotation without closing parenthesis in expressions
# Pattern: (x : Type op ... where op is not ) and there's no closing )
# Fix common patterns

# Fix Real:= → Real :=
content = content.replace('Real:=', 'Real :=')
content = content.replace('ℝ:=', 'ℝ :=')

# Fix (x : Real = ...  → (x : Real) = ... (when used in type annotation context)
# This is tricky - need to match cases where the ) is missing
content = re.sub(r'\((\d+\s*:\s*Real)\s*([\+\-\*/<>=∧∨≠≤≥])', r'(\1) \2', content)
content = re.sub(r'\((\w+\s*:\s*Real)\s*([\+\-\*/<>=∧∨≠≤≥])', r'(\1) \2', content)
content = re.sub(r'\((\w+\s*:\s*ℝ)\s*([\+\-\*/<>=∧∨≠≤≥])', r'(\1) \2', content)

# Fix |(... : Real - ...| → |(... : Real) - ...|
content = re.sub(r'\|(\([^|]*:\s*Real)\s*-\s*([^|]*)\|', r'|(\1) - \2|', content)
content = re.sub(r'\|(\([^|]*:\s*ℝ)\s*-\s*([^|]*)\|', r'|(\1) - \2|', content)

# Fix (x : Real * y → (x : Real) * y
content = re.sub(r'\(([^)]*:\s*Real)\s*\*', r'(\1) *', content)
content = re.sub(r'\(([^)]*:\s*ℝ)\s*\*', r'(\1) *', content)

# Fix (x : Real) * phi → (x : Real) * phi (already fixed above)

# Fix ≠( → ≠ (
content = content.replace('≠(', '≠ (')
content = content.replace('≠(', '≠ (')

# Fix structure Debt where value : Real  rate : Real  time : Real
content = content.replace('value : Real  rate : Real  time : Real', 'value : Real\n  rate : Real\n  time : Real')

# Fix phi_cantor_dimension_approx comment
content = content.replace('≠1.44', 'approx 1.44')

# Write the fixed file
with open(r'C:\Users\一梦\.kimi_openclaw\workspace\sylva_formalization\SylvaFormalization\Basic.lean', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed Basic.lean")
