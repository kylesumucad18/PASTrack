import re

file_path = 'core/templates/core/case_detail.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines):
    opens = len(re.findall(r'<div\b', line))
    closes = len(re.findall(r'</div\b', line))
    depth += (opens - closes)
    if depth < 0:
        print(f"Line {i+1}: Depth dropped to {depth}. Line: {line.strip()}")
        # Just reset to 0 so we can find all points where an extra </div> exists
        depth = 0

print("Finished checking depth.")
