with open('Basic.lean', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\\n', '\n')
print('sorry count in Basic.lean:', content.count('sorry'))
print('import count:', content.count('import'))
