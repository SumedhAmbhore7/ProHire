from django.shortcuts import render, redirect
from .models import Job, Application
from django.contrib.auth.decorators import login_required
from users.decorators import hr_required

from .forms import JobForm

@login_required
@hr_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.status = 'active' # Auto-approve jobs posted by HR
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})

from django.db.models import Q

def job_list(request):
    jobs = Job.objects.filter(status='active').order_by('-created_at')
    
    # Search Filter
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(location__icontains=query))

    # Recommendations (Skill Matching)
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.skills:
        user_skills = [s.strip().lower() for s in request.user.userprofile.skills.split(',') if s.strip()]
        
        # Calculate match score for each job
        # Note: This is a simple Python-side implementation. For production, DB-level matching is better.
        job_list_with_scores = []
        for job in jobs:
            job_skills = [s.strip().lower() for s in job.skills_required.split(',') if s.strip()]
            match_count = sum(1 for skill in user_skills if skill in job_skills)
            job.match_score = match_count
            job_list_with_scores.append(job)
            
        # Sort by match score (descending) then by creation date (descending)
        jobs = sorted(job_list_with_scores, key=lambda x: (x.match_score, x.created_at), reverse=True)

    applied_job_ids = []
    if request.user.is_authenticated and not hasattr(request.user, 'hrprofile'):
        applied_job_ids = Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)
        
    return render(request, 'job_list.html', {'jobs': jobs, 'applied_job_ids': applied_job_ids, 'query': query})

from django.contrib import messages

@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
    else:
        Application.objects.create(job=job, applicant=request.user)
        messages.success(request, 'Successfully applied for the job!')
    return redirect('job_list')

@login_required
@hr_required
def employer_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'employer_dashboard.html', {'jobs': jobs})

@login_required
@hr_required
def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if job.posted_by != request.user:
        messages.error(request, "You are not authorized to edit this job.")
        return redirect('employer_dashboard')
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'post_job.html', {'form': form, 'title': 'Edit Job'})

@login_required
@hr_required
def delete_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if job.posted_by != request.user:
        messages.error(request, "You are not authorized to delete this job.")
        return redirect('employer_dashboard')
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect('employer_dashboard')
    return render(request, 'confirm_delete.html', {'job': job})

@login_required
@hr_required
def update_application_status(request, application_id, new_status):
    application = Application.objects.get(id=application_id)
    if application.job.posted_by != request.user:
        messages.error(request, "Unauthorized action.")
        return redirect('employer_dashboard')
    
    if new_status in ['accepted', 'rejected']:
        application.status = new_status
        application.save()
        messages.success(request, f"Application marked as {new_status}.")
    return redirect('employer_dashboard')