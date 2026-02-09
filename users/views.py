from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile, HRProfile

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        role = request.POST.get('role', 'seeker')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already connected to an account'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        if role == 'employer':
            company = request.POST.get('company', '')
            HRProfile.objects.create(user=user, company=company, phone=phone)
        else:
            resume = request.FILES.get('resume')
            UserProfile.objects.create(user=user, phone=phone, resume=resume)
            
        return redirect('users:login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('job_list')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('users:login')

from django.contrib.auth.decorators import login_required
from .forms import SeekerProfileForm, HRProfileForm
from jobs.models import Application

@login_required
def profile(request):
    user = request.user
    if hasattr(user, 'hrprofile'):
        # HR Profile
        instance = user.hrprofile
        if request.method == 'POST':
            form = HRProfileForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('users:profile')
        else:
            form = HRProfileForm(instance=instance)
        
        # Get Posted Jobs for Dashboard
        from jobs.models import Job
        jobs = Job.objects.filter(posted_by=user)
        return render(request, 'users/profile.html', {'form': form, 'is_hr': True, 'jobs': jobs})
    
    elif hasattr(user, 'userprofile'):
        # Seeker Profile
        instance = user.userprofile
        if request.method == 'POST':
            form = SeekerProfileForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('users:profile')
        else:
            form = SeekerProfileForm(instance=instance)
            
        # Get Applied Jobs
        applications = Application.objects.filter(applicant=user).select_related('job').order_by('-applied_at')
        return render(request, 'users/profile.html', {'form': form, 'is_hr': False, 'applications': applications})
    
    return redirect('home')
