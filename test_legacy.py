
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legaltrack.settings')
django.setup()
from core.models import Case, CaseDocument

latest = Case.objects.filter(is_legacy_override=True).order_by('-created_at').first()
if latest:
    print('Latest Legacy Case:', latest.tracking_id, latest.id)
    print('is_legacy_override:', latest.is_legacy_override)
    docs = CaseDocument.objects.filter(case=latest)
    print('Docs count:', docs.count())
    for d in docs:
        print(' - Doc:', d.doc_type, 'File:', d.file.name if d.file else None)
    print('Property call:', latest.legacy_document_scan)
else:
    print('No legacy cases found')

