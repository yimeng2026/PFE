import sys

with open(sys.argv[1], 'rb') as f:
    data = f.read()

# Find bytes around 鈩 (U+9229 = UTF-8 E9 88 A9)
idx = data.find(bytes([0xe9, 0x88, 0xa9]))
if idx != -1:
    segment = data[idx:idx+12]
    print("Bytes around 鈩:", segment.hex())
    print("Decoded:", segment.decode("utf-8", errors="replace"))

# Also check 鈭 (U+922D = E9 88 AD)
idx2 = data.find(bytes([0xe9, 0x88, 0xad]))
if idx2 != -1:
    segment2 = data[idx2:idx2+12]
    print("Bytes around 鈭:", segment2.hex())
    print("Decoded:", segment2.decode("utf-8", errors="replace"))
