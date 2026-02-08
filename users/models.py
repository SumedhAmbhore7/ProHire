from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes', blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills (e.g. Python, Django)")

class HRProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
