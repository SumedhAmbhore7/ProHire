from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile, HRProfile
from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings

from django.core import mail

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.password_reset_url = reverse('password_reset') # Built-in, no namespace here

    def test_password_reset(self):
        """Test password reset flow"""
        # Create a user to reset password for
        User.objects.create_user(username='reset_user', email='reset@example.com', password='oldpass')
        
        # 1. Get reset page
        response = self.client.get(self.password_reset_url)
        self.assertEqual(response.status_code, 200)
        
        # 2. Post email
        response = self.client.post(self.password_reset_url, {'email': 'reset@example.com'})
        self.assertEqual(response.status_code, 302) # Redirects to done
        
        # 3. Check email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password reset', mail.outbox[0].subject)

    def test_job_seeker_registration_with_resume(self):
        """Test registration as a Job Seeker with resume"""
        resume_content = b'This is a test resume content'
        resume = SimpleUploadedFile("resume.txt", resume_content, content_type="text/plain")
        
        response = self.client.post(self.register_url, {
            'username': 'seeker',
            'password': 'password123',
            'phone': '1234567890',
            'role': 'seeker',
            'resume': resume
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(UserProfile.objects.filter(user__username='seeker').exists())
        profile = UserProfile.objects.get(user__username='seeker')
        self.assertTrue(bool(profile.resume))
        
        # Cleanup
        if profile.resume:
            if os.path.isfile(profile.resume.path):
                os.remove(profile.resume.path)

        if profile.resume:
            if os.path.isfile(profile.resume.path):
                os.remove(profile.resume.path)

    def test_login(self):
        """Test user login"""
        user = User.objects.create_user(username='testuser', password='password123')
        UserProfile.objects.create(user=user, phone='0000000000')
        
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302) # Redirects to job_list

    def test_profile_view(self):
        """Test profile page for Seeker and HR"""
        # Test Seeker Profile
        seeker = User.objects.create_user(username='profile_seeker', password='password123')
        UserProfile.objects.create(user=seeker, phone='123')
        self.client.login(username='profile_seeker', password='password123')
        
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['is_hr'])
        
        # Test Profile Update (Seeker)
        response = self.client.post(reverse('users:profile'), {
            'phone': '9999999999',
            'skills': 'New Skill'
        })
        self.assertEqual(response.status_code, 302)
        seeker.userprofile.refresh_from_db()
        self.assertEqual(seeker.userprofile.phone, '9999999999')
        self.assertEqual(seeker.userprofile.skills, 'New Skill')
        
        self.client.logout()
        
        # Test HR Profile
        hr = User.objects.create_user(username='profile_hr', password='password123')
        HRProfile.objects.create(user=hr, company='Old Corp', phone='123')
        self.client.login(username='profile_hr', password='password123')
        
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_hr'])
        self.assertIn('jobs', response.context)
        
        # Test Profile Update (HR)
        response = self.client.post(reverse('users:profile'), {
            'company': 'New Corp',
            'phone': '8888888888'
        })
        self.assertEqual(response.status_code, 302)
        hr.hrprofile.refresh_from_db()
        self.assertEqual(hr.hrprofile.company, 'New Corp')
