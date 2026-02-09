from jobs.models import Job
count = Job.objects.filter(status='pending').update(status='active')
print(f"Successfully activated {count} pending jobs.")
