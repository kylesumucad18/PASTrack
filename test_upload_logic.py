import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legaltrack.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS = ['*']

from django.test import Client
from core.models import CustomUser, Case

user = CustomUser.objects.first()
user.role = 'lgu_admin'
user.save()

client = Client()
client.force_login(user)

with open('test.png', 'wb') as f:
    f.write(b'fake image data')

with open('test.png', 'rb') as fp:
    response = client.post('/submit/', {
        'ownership_type': 'single',
        'client_first_name': 'Test12345',
        'client_last_name': 'User',
        'client_number': '09123456789',
        'case_type': 'transfer_ownership_tax_decl',
        'property_title_type': 'titled',
        'classification': 'residential',
        'lot_number': '123',
        'is_legacy_override': True,
        'previous_tax_dec_number': '12345',
        'original_area': 100,
        'transferred_area': 100,
        'area_unit': 'sqm',
        'area_value': 100,
        'save_continue': 'Continue',
        'legacy_document_scan': fp
    })

print('Response Status:', response.status_code)
html = response.content.decode('utf-8')
if 'class="errorlist"' in html or 'error-msg' in html:
    print('FOUND ERRORS IN HTML')
    lines = html.split('\n')
    for i, line in enumerate(lines):
        if 'error-msg' in line or 'errorlist' in line:
            print(line.strip())

latest = Case.objects.filter(is_legacy_override=True, client_first_name='Test12345').order_by('-created_at').first()
if latest:
    print('Docs count:', latest.documents.count())
    for d in latest.documents.all():
        print(d.doc_type, d.file.name)
