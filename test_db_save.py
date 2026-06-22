import os
import django
from django.core.files.base import ContentFile
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "legaltrack.settings")
django.setup()

from core.models import Case, CaseDocument

case = Case.objects.first()
if case:
    # Get or create
    doc, created = CaseDocument.objects.get_or_create(case=case, doc_type="test4")
    
    # Save a word file directly
    doc.file.save("existing.docx", ContentFile(b"old content", name="existing.docx"))
    print("DB value before:", CaseDocument.objects.get(id=doc.id).file.name)
    
    # Now simulate the update exactly like _upsert_case_document
    final_file = ContentFile(b"fake pdf content 4", name="test4.pdf")
    doc.file = final_file
    doc.save(update_fields=["file", "updated_at"])
    
    print("DB value after:", CaseDocument.objects.get(id=doc.id).file.name)
else:
    print("No case found to test")
