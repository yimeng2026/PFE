with open('NavierStokes.lean', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all backslash characters and their context
idx = 0
found = 0
while idx < len(content):
    idx = content.find('\\', idx)
    if idx < 0:
        break
    start = max(0, idx-5)
    end = min(len(content), idx+10)
    with open('backslash_context.txt', 'a', encoding='utf-8') as out:
        out.write(f'[{idx}] {repr(content[start:end])}\n')
    found += 1
    idx += 1

print(f'Found {found} backslash characters')
