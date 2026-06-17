with open('NavierStokes.lean', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if any backslash is NOT followed by n
idx = 0
bad = 0
while idx < len(content):
    idx = content.find('\\', idx)
    if idx < 0:
        break
    if idx + 1 < len(content) and content[idx + 1] != 'n':
        bad += 1
        print(f'Bad backslash at {idx}: {repr(content[idx:idx+5])}')
    idx += 1

print(f'Bad backslashes: {bad}')
