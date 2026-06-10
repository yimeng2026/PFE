import sys, os, re, json

# Character mapping based on analysis
def analyze_file(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
    
    # Find all non-ASCII characters
    non_ascii = {}
    for i, b in enumerate(content):
        if b > 127:
            # Get the surrounding context
            start = max(0, i-5)
            end = min(len(content), i+10)
            ctx = content[start:end]
            try:
                ctx_str = ctx.decode('utf-8', errors='replace')
            except:
                ctx_str = str(ctx)
            if ctx_str not in non_ascii:
                non_ascii[ctx_str] = 0
            non_ascii[ctx_str] += 1
    
    return non_ascii

# Analyze Basic.lean
filepath = "C:/Users/一梦/.kimi_openclaw/workspace/sylva_formalization/SylvaFormalization/Basic.lean"
result = analyze_file(filepath)

# Print unique non-ASCII sequences
with open("C:/Users/一梦/.kimi_openclaw/workspace/sylva_formalization/encoding_analysis.txt", "w", encoding="utf-8") as out:
    for ctx, count in sorted(result.items(), key=lambda x: -x[1])[:50]:
        out.write(f"{count:4d} | {repr(ctx)}\n")
