with open('SylvaFormalization/NavierStokes.lean', 'r', encoding='utf-8') as f:
    lines = f.readlines()
with open('line_check.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(lines[20:35], start=21):
        f.write(f'{i}: {repr(line)}\n')
print('Done')
