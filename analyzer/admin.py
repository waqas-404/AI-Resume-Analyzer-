from django.contrib import admin
from .models import ResumeAnalysis

@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'similarity_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['job_description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']