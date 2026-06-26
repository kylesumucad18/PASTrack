import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legaltrack.settings')
django.setup()
from core.models import Case

cases = Case.objects.filter(lot_number='NA')
count = cases.update(lot_number="")
cases2 = Case.objects.filter(previous_tax_dec_number='NA')
count2 = cases2.update(previous_tax_dec_number="")

print(f"Cleared 'NA' from {count} lot_numbers and {count2} previous_tax_dec_numbers.")
