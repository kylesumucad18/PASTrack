
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legaltrack.settings')
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from core.forms import CaseDetailsForm
from core.models import Case, CustomUser

user = CustomUser.objects.first()

file_data = b'test file content'
upload = SimpleUploadedFile('test.png', file_data, content_type='image/png')

data = {
    'ownership_type': 'individual',
    'client_first_name': 'Test',
    'client_last_name': 'User',
    'case_type': 'transfer_ownership_tax_decl',
    'classification': 'residential',
    'is_legacy_override': True,
    'previous_tax_dec_number': '12345',
}
files = {'legacy_document_scan': upload}

form = CaseDetailsForm(data=data, files=files, user=user)
print('is_valid:', form.is_valid())
if not form.is_valid():
    print('Errors:', form.errors)
else:
    print('Cleaned legacy_document_scan:', form.cleaned_data.get('legacy_document_scan'))

