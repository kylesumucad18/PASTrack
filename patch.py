import os
import re

filepath = r'c:\Users\Kyle\Desktop\projects\pastrack-versions\cloneD\PASTrack\core\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Pagination
content = content.replace('paginator = Paginator(qs, 15)', 'paginator = Paginator(qs, 10)')
content = content.replace('paginator = Paginator(qs, 20)', 'paginator = Paginator(qs, 10)')

# Regex to fix the tabs for scope == "me"
# Search for: ("something", f"Something ({some_qs.count()})")
# Replace with: ("something", "Something", some_qs.count())
pattern = r'\(\s*"([^"]+)"\s*,\s*f"([^\(]+)\s*\(\{([^\}]+)\}\)"\s*\)'
# explanation of pattern:
# group 1: tab_id
# group 2: tab_label
# group 3: count_expr

def replacer(match):
    tab_id = match.group(1)
    tab_label = match.group(2).strip()
    count_expr = match.group(3)
    return f'("{tab_id}", "{tab_label}", {count_expr})'

content = re.sub(pattern, replacer, content)

# Fix scope == "all" tabs
old_all_tabs = '''        tabs = [
            ("all", "All"), ("pending", "Pending"), ("received", "Received"),
            ("to_examine", "To Examine"), ("for_taxmapping", "For Taxmapping"),
            ("for_approval", "For Approval"), ("for_numbering", "For Numbering"),
            ("for_release", "For Release"), ("released", "Released"),
        ]'''

new_all_tabs = '''        tabs = [
            ("all", "All", qs.count()),
            ("pending", "Pending", qs.filter(status__in=["not_received", "client_correction"]).count()),
            ("received", "Received", qs.filter(status="received", assigned_to__isnull=True).count()),
            ("to_examine", "To Examine", qs.filter(status__in=["to_examine", "in_review"]).count()),
            ("for_taxmapping", "For Taxmapping", qs.filter(status="for_taxmapping").count()),
            ("for_approval", "For Approval", qs.filter(status="for_approval").count()),
            ("for_numbering", "For Numbering", qs.filter(status="for_numbering").count()),
            ("for_release", "For Release", qs.filter(status="for_release").count()),
            ("released", "Released", qs.filter(status="released").count()),
        ]'''

content = content.replace(old_all_tabs, new_all_tabs)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patch applied successfully.")
