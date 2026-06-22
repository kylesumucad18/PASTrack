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
    doc, created = CaseDocument.objects.get_or_create(case=case, doc_type="test3")
    
    # Simulate an existing file
    doc.file.save("existing.docx", ContentFile(b"old content", name="existing.docx"))
    
    # Now simulate the update
    final_file = ContentFile(b"fake pdf content 3", name="test3.pdf")
    doc.file = final_file
    doc.updated_at = timezone.now()
    doc.save(update_fields=["file", "updated_at"])
    
    print("Saved doc file name:", doc.file.name)
    if doc.file and hasattr(doc.file, 'path') and os.path.exists(doc.file.path):
        print("File exists on disk:", doc.file.path)
    elif doc.file and doc.file.name:
        from django.core.files.storage import default_storage
        if default_storage.exists(doc.file.name):
            print("File exists in storage:", doc.file.name)
        else:
            print("FILE IS MISSING FROM STORAGE!")
else:
    print("No case found to test")
