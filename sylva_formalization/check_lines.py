import sys

filepath = "C:/Users/一梦/.kimi_openclaw/workspace/sylva_formalization/SylvaFormalization/Basic.lean"

with open(filepath, 'rb') as f:
    content = f.read()

# Clear output file
with open("C:/Users/一梦/.kimi_openclaw/workspace/sylva_formalization/line_check.txt", "w", encoding="utf-8") as out:
    pass

# Find line 210-220 (0-indexed: 209-219)
lines = content.split(b'\n')
for i in range(209, 220):
    if i < len(lines):
        line = lines[i]
        hex_str = ' '.join(f'{b:02x}' for b in line)
        try:
            utf8 = line.decode('utf-8', errors='replace')
        except:
            utf8 = "<error>"
        with open("C:/Users/一梦/.kimi_openclaw/workspace/sylva_formalization/line_check.txt", "a", encoding="utf-8") as out:
            out.write(f"Line {i+1}: {hex_str[:100]}\n")
            out.write(f"  UTF-8: {utf8[:120]}\n\n")
