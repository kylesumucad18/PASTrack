import re

file_path = 'core/templates/core/case_detail.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for the old inline modal loaders.
# They look like:
# <!-- Loader UI Overlay -->
# <div class="premium-modal-loader"...> ... </div>
pattern1 = re.compile(r'<!-- Loader UI Overlay -->\s*<div class="premium-modal-loader".*?</div>', re.DOTALL)
pattern2 = re.compile(r'<!-- Loader UI Overlay -->\s*<div id="examinerForwardLoader".*?</div>', re.DOTALL)

content = re.sub(pattern1, '', content)
content = re.sub(pattern2, '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed inline modal loaders from case_detail.html")
