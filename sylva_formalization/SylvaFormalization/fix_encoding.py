import os
import glob

for f in glob.glob("*.lean"):
    with open(f, "rb") as fh:
        data = fh.read()
    
    # Check for UTF-16 LE null bytes
    if b'\x00' in data[:100]:
        print(f"{f}: Contains null bytes")
        try:
            # Try UTF-16 LE
            text = data.decode("utf-16-le")
            # Save as UTF-8
            with open(f, "w", encoding="utf-8") as out:
                out.write(text)
            print(f"  Fixed: UTF-16 LE -> UTF-8")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print(f"{f}: No null bytes, likely OK or different encoding")
