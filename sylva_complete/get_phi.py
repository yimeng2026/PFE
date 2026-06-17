with open('BasicTutorial.lean', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\\n', '\n')
idx = content.find('namespace Phi')
if idx >= 0:
    end_idx = content.find('end Phi', idx)
    with open('phi_snippet.txt', 'w', encoding='utf-8') as f:
        f.write(content[idx:end_idx+20])
    print('Wrote phi_snippet.txt')
