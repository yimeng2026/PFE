import os

def strip_bom(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        with open(filepath, 'wb') as f:
            f.write(raw[3:])
        return True
    return False

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.lean'):
            filepath = os.path.join(root, file)
            if strip_bom(filepath):
                print(f'Stripped BOM from {filepath}')

print('Done')
