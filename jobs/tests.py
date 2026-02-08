from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.models import HRProfile, UserProfile
from .models import Job, Application
from django.urls import reverse

class JobTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create HR User
        self.hr_user = User.objects.create_user(username='hr_user', password='password123')
        HRProfile.objects.create(user=self.hr_user, company='TechCorp', phone='1234567890')
        
        # Create Job Seeker User
        self.seeker_user = User.objects.create_user(username='seeker_user', password='password123')
        UserProfile.objects.create(user=self.seeker_user, phone='0987654321')

        self.post_job_url = reverse('post_job')
        self.job_list_url = reverse('job_list')

    def test_hr_can_post_job(self):
        """Test that HR user can post a job (default pending)"""
        self.client.login(username='hr_user', password='password123')
        response = self.client.post(self.post_job_url, {
            'title': 'Test Job',
            'company': 'TechCorp',
            'location': 'Remote',
            'salary': '$1000',
            'description': 'Test Description',
            'skills_required': 'Python' 
        })
        self.assertEqual(response.status_code, 302) # Success redirect
        # Verify job is active by default
        job = Job.objects.get(title='Test Job')
        self.assertEqual(job.status, 'active')

    def test_seeker_cannot_post_job(self):
        """Test that Job Seeker cannot post a job"""
        self.client.login(username='seeker_user', password='password123')
        response = self.client.get(self.post_job_url)
        # Should redirect to home or some other page due to @hr_required
        self.assertNotEqual(response.status_code, 200) 
        self.assertEqual(response.status_code, 302)

    def test_seeker_can_apply(self):
        """Test that Job Seeker can apply for a job"""
        # First creating a job
        job = Job.objects.create(
            title='Existing Job',
            company='Corp',
            location='City',
            salary='$500', 
            description='Desc', 
            posted_by=self.hr_user,
            status='active' # Must be active to confirm existence in public workflows
        )
        
        self.client.login(username='seeker_user', password='password123')
        apply_url = reverse('apply_job', args=[job.id])
        response = self.client.get(apply_url)
        
        self.assertEqual(response.status_code, 302) # Redirects after applying
        self.assertTrue(Application.objects.filter(job=job, applicant=self.seeker_user).exists())

    def test_job_list_shows_applied_status(self):
        """Test that job list context contains applied job IDs"""
        job = Job.objects.create(
            title='Job 1', company='C1', location='L1', salary='S1', description='D1', posted_by=self.hr_user, status='active'
        )
        Application.objects.create(job=job, applicant=self.seeker_user)
        
        self.client.login(username='seeker_user', password='password123')
        response = self.client.get(self.job_list_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('applied_job_ids', response.context)
        self.assertIn(job.id, response.context['applied_job_ids'])

    def test_employer_dashboard(self):
        """Test employer dashboard access and content"""
        self.client.login(username='hr_user', password='password123')
        job = Job.objects.create(
            title='My Job', company='TechCorp', location='Remote', salary='$1000', description='Desc', posted_by=self.hr_user
        )
        dashboard_url = reverse('employer_dashboard')
        response = self.client.get(dashboard_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('jobs', response.context)
        self.assertIn(job, response.context['jobs'])

    def test_job_search(self):
        """Test job search functionality"""
        Job.objects.create(title='Python Dev', company='A', location='Loc1', salary='100', posted_by=self.hr_user, description='Desc', status='active')
        Job.objects.create(title='Java Dev', company='B', location='Loc2', salary='100', posted_by=self.hr_user, description='Desc', status='active')
        
        response = self.client.get(self.job_list_url, {'q': 'Python'})
        self.assertEqual(len(response.context['jobs']), 1)
        self.assertEqual(response.context['jobs'][0].title, 'Python Dev')

    def test_job_recommendations(self):
        """Test skill-based recommendations"""
        # Add skills to seeker
        self.seeker_profile = UserProfile.objects.get(user=self.seeker_user)
        self.seeker_profile.skills = 'Python, Django'
        self.seeker_profile.save()
        
        # Create jobs with and without matching skills
        job_match = Job.objects.create(title='Match', company='A', location='L', salary='1', posted_by=self.hr_user, skills_required='Python', description='Desc', status='active')
        job_no_match = Job.objects.create(title='No Match', company='B', location='L', salary='1', posted_by=self.hr_user, skills_required='Java', description='Desc', status='active')
        
        self.client.login(username='seeker_user', password='password123')
        response = self.client.get(self.job_list_url)
        
        # Check sort order (match first)
        jobs = response.context['jobs']
        self.assertEqual(jobs[0].title, 'Match')
        self.assertEqual(getattr(jobs[0], 'match_score', 0), 1)
        self.assertEqual(getattr(jobs[1], 'match_score', 0), 0)

    def test_login_required(self):
        """Test that login is required for protected views"""
        self.client.logout()
        
        # Post Job
        response = self.client.get(self.post_job_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)
        
        # Apply Job
        job = Job.objects.create(title='Job', company='C', location='L', salary='S', posted_by=self.hr_user, status='active')
        apply_url = reverse('apply_job', args=[job.id])
        response = self.client.get(apply_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)
        
        # Employer Dashboard
        dashboard_url = reverse('employer_dashboard')
        response = self.client.get(dashboard_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)
