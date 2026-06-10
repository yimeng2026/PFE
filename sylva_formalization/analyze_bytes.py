import sys, os, re, json

# Analyze specific byte sequences around garbled characters
def analyze_bytes(filepath, target_positions):
    with open(filepath, 'rb') as f:
        content = f.read()
    
    results = []
    for pos in target_positions:
        start = max(0, pos - 10)
        end = min(len(content), pos + 15)
        byte_slice = content[start:end]
        hex_str = ' '.join(f'{b:02x}' for b in byte_slice)
        try:
            utf8_str = byte_slice.decode('utf-8', errors='replace')
        except:
            utf8_str = "<decode error>"
        try:
            gbk_str = byte_slice.decode('gbk', errors='replace')
        except:
            gbk_str = "<decode error>"
        results.append((pos, hex_str, utf8_str, gbk_str))
    
    return results

filepath = "C:/Users/一梦/.kimi_openclaw/workspace/sylva_formalization/SylvaFormalization/Basic.lean"

# Find positions of replacement characters or high-byte sequences
with open(filepath, 'rb') as f:
    content = f.read()

positions = []
for i, b in enumerate(content):
    if b == 0xef or b == 0xbf or b == 0xfd:  # Common UTF-8 replacement bytes
        if i not in positions and i > 0:
            positions.append(i)

# Also find positions around "ℝ" which is correct
for i in range(len(content) - 2):
    if content[i:i+3] == b'\xe2\x84\x9d':  # ℝ
        if i not in positions:
            positions.append(i)

positions = sorted(positions)[:30]

results = analyze_bytes(filepath, positions)

with open("C:/Users/一梦/.kimi_openclaw/workspace/sylva_formalization/byte_analysis.txt", "w", encoding="utf-8") as out:
    for pos, hex_str, utf8, gbk in results:
        out.write(f"Pos {pos}: {hex_str}\n")
        out.write(f"  UTF-8: {repr(utf8)}\n")
        out.write(f"  GBK:   {repr(gbk)}\n\n")
