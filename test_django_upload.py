import os
import django
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "legaltrack.settings")
django.setup()

from core.views import _maybe_convert_office_upload_to_pdf

# Make a small docx file
with open('test_valid.docx', 'rb') as f:
    file_content = f.read()

uploaded_file = SimpleUploadedFile("test_valid.docx", file_content, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

final_file, convert_info = _maybe_convert_office_upload_to_pdf(uploaded_file)

print("Convert info:", convert_info)
if final_file and hasattr(final_file, "name"):
    print("Final file name:", final_file.name)
