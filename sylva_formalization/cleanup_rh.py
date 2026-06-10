with open('SylvaFormalization/RiemannHypothesis.lean', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the duplicate text - there are two identical doc comment blocks before theorem zero_symmetry
# Find the first one (ends with -/) and remove everything from there to the second -/ before theorem zero_symmetry
marker1 = "    if ρ is a zero, so is 1 - ρ."
marker2 = "theorem zero_symmetry"

if marker1 in content and marker2 in content:
    # Find first occurrence of marker1 after a -/ 
    idx1 = content.find(marker1)
    idx2 = content.find(marker2)
    if idx1 < idx2 and idx1 > 0:
        # Find the -/ before marker1
        idx_comment_end = content.rfind("-/", 0, idx1)
        if idx_comment_end > 0:
            # Remove from idx_comment_end+2 to idx2 (keeping the second block intact)
            # Actually, find the second -/ before idx2
            idx_second_comment_end = content.rfind("-/", 0, idx2)
            if idx_second_comment_end > idx_comment_end:
                content = content[:idx_comment_end+2] + content[idx2:]
                print(f"Removed duplicate block from {idx_comment_end+2} to {idx2}")
            else:
                print("Could not find second comment end")
        else:
            print("Could not find first comment end")
    else:
        print("Markers not in expected order")
else:
    print("Markers not found")

with open('SylvaFormalization/RiemannHypothesis.lean', 'w', encoding='utf-8') as f:
    f.write(content)
