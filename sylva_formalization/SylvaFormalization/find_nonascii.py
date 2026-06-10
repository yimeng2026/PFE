with open("Basic.lean", "rb") as f:
    data = f.read(500)

# Find positions of non-ASCII bytes
for i, b in enumerate(data):
    if b > 0x7F:
        context = data[max(0,i-10):min(len(data), i+10)]
        print(f"Byte 0x{b:02x} at position {i}")
        print(f"  Context (hex): {context.hex()}")
        try:
            print(f"  Context (utf8): {context.decode('utf-8')}")
        except:
            print(f"  Context (latin1): {context.decode('latin-1')}")
        print()
        if i > 50:
            break
