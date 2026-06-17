with open('NavierStokes.lean', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all literal backslash-n sequences with actual newlines
content = content.replace('\\n', '\n')

with open('NavierStokes.lean', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done. Actual newline count:', content.count('\n'))
