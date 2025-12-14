from django import forms
from .models import ResumeAnalysis

class ResumeAnalysisForm(forms.ModelForm):
    class Meta:
        model = ResumeAnalysis
        fields = ['resume', 'job_description']
        widgets = {
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Paste the complete job description here...'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            })
        }