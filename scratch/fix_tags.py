import re

def fix_template_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Loop to replace multiline {% %} until there are no more newlines
    prev = None
    while content != prev:
        prev = content
        content = re.sub(r'(\{%[^%}]*?)\r?\n([^%}]*?%\})', r'\1 \2', content)

    # Loop to replace multiline {{ }} until there are no more newlines
    prev = None
    while content != prev:
        prev = content
        content = re.sub(r'(\{\{[^}]*?)\r?\n([^}]*?\}\})', r'\1 \2', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_template_tags('core/templates/core/case_detail.html')
