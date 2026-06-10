import re, sys

# Read file
with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Mapping based on deeper context analysis
replacements = {
    '鈩?': 'Real',      # Type: a : Real, phi : Real := ...
    '鈭?': '∃',          # Existential quantifier: ∃ n > 0, ...
    '鈭€': '∀',          # Universal quantifier: ∀ i, c i = 0
    '鈫?': '→',          # Function arrow: Fin r → Real
    '鈮?': '≠',          # Not equal: E.discriminant ≠ 0
    '鈥?': '*',          # Multiplication: n * x = 0
    '路': ' * ',         # Multiplication in formulas
    '虏': '^ 2',         # Square
    '鲁': '^ 3',         # Cube
    '蠁': 'phi',         # Golden ratio
    '螖': 'Δ',           # Discriminant
    '蟺': 'π',           # Pi
    '桅': 'ζ',           # Zeta
    '楔': 'Sha',         # Tate-Shafarevich group
    '螞': 'Λ',           # Completed L-function
    '磨': 'h',           # Canonical height
    '惟': 'ω',           # Real period
    '≒': '≈',
    '€': 'α',            # Greek alpha (tentative)
    '脳': '*',
    '廮': '∏',           # Product
    'な': '∃',
    '鈯?': '∃',
    '鈦宦?': '⁻¹',      # Inverse: phi⁻¹ = phi - 1
    '鉄': '<',
    '茅': 'N',
    '乆': '₁',           # Subscript 1
    '僘': '₃',           # Subscript 3
    '俋': '₂',           # Subscript 2
    '刋': '₄',           # Subscript 4
    '鈥': '*',
    '鈱': '?',
    '螕': '?',
    '蔚': '?',
    '鹿': '?',
    'ぢ': '?',
    '肺': '?',
    '': '?',
    '胃': '?',
    '廲': '?',
    '圿': '?',
    '卤': '?',
    '危': '?',
    '掆': '?',
    '垶': '?',
    '≦': '≤',
    '╩': '?',
    '': '?',
    '': '?',
    '亁': '?',
    '皚': '?',
    '倉': '?',
    '儅': '?',
    '毼': '?',
    '': '?',
    '個': '?',
    '妉': '?',
    '‥': '?',
}

# Sort by length descending to avoid partial matches
for old, new in sorted(replacements.items(), key=lambda x: -len(x[0])):
    content = content.replace(old, new)

# Fix spacing around arrows: ensure → has spaces
content = re.sub(r'(?<!\s)→(?!\s)', ' → ', content)
content = re.sub(r'(?<!\s)←(?!\s)', ' ← ', content)

# Write output
with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print(f"Wrote {sys.argv[2]}")
