import sys

filepath = "C:/Users/一梦/.kimi_openclaw/workspace/sylva_formalization/SylvaFormalization/Basic.lean"

with open(filepath, 'rb') as f:
    content = f.read()

lines = content.split(b'\n')

with open("C:/Users/一梦/.kimi_openclaw/workspace/sylva_formalization/line213_full.txt", "w", encoding="utf-8") as out:
    for i in [212, 213, 214, 215, 292, 293, 294, 295, 296, 305, 306, 307]:
        if i < len(lines):
            line = lines[i]
            hex_full = ' '.join(f'{b:02x}' for b in line)
            try:
                utf8 = line.decode('utf-8', errors='replace')
            except:
                utf8 = "<error>"
            out.write(f"Line {i+1} ({len(line)} bytes):\n")
            out.write(f"  HEX: {hex_full}\n")
            out.write(f"  UTF8: {utf8}\n\n")
