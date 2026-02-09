import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProHire.settings')
django.setup()

from jobs.models import Job

# Check counts
total = Job.objects.count()
active = Job.objects.filter(status='active').count()
pending = Job.objects.filter(status='pending').count()
rejected = Job.objects.filter(status='rejected').count()

print(f"Total Jobs: {total}")
print(f"Active: {active}")
print(f"Pending: {pending}")
print(f"Rejected: {rejected}")
