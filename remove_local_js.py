import re

file_path = 'core/templates/core/case_detail.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the previous local loader script and remove it.
# The local script was added in case_detail.html and starts with:
# <script>
# (function () {
#   let fakeTimer = null;
#   let currentPct = 0;
#   function setProgress(loaderBlock, pct) {
# ...

pattern = re.compile(r'<script>\s*\(function \(\) \{\s*let fakeTimer = null;\s*let currentPct = 0;.*?\)\(\);\s*</script>', re.DOTALL)

content = re.sub(pattern, '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed local loader script from case_detail.html")
