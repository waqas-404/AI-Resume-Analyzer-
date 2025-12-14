from django.db import models
from django.core.validators import FileExtensionValidator

class ResumeAnalysis(models.Model):
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    job_description = models.TextField()
    similarity_score = models.FloatField(null=True, blank=True)
    job_keywords = models.JSONField(null=True, blank=True)
    resume_keywords = models.JSONField(null=True, blank=True)
    missing_keywords = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Analysis {self.id} - Score: {self.similarity_score}%"