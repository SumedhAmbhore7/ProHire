from django import forms
from .models import UserProfile, HRProfile

class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'resume', 'skills']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, SQL'}),
        }

class HRProfileForm(forms.ModelForm):
    class Meta:
        model = HRProfile
        fields = ['company', 'phone']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
