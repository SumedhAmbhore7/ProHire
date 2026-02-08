from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from jobs.models import Job, Application

@user_passes_test(lambda u: u.is_superuser)
def analytics_dashboard(request):
    total_seekers = User.objects.filter(userprofile__isnull=False).count()
    total_employers = User.objects.filter(hrprofile__isnull=False).count()
    total_jobs = Job.objects.count()
    active_jobs = Job.objects.filter(status='active').count()
    pending_jobs = Job.objects.filter(status='pending').count()
    total_applications = Application.objects.count()
    
    context = {
        'total_seekers': total_seekers,
        'total_employers': total_employers,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'pending_jobs': pending_jobs,
        'total_applications': total_applications,
    }
    return render(request, 'adminpanel/dashboard.html', context)
