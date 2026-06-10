import re, sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Fix missing ) after type annotations like (expr : Real)
# Pattern: ( ... : Real not followed by )
content = re.sub(r'(\([^)]* : Real)(?!\))', r'\1)', content)

with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print(f"Wrote {sys.argv[2]}")
