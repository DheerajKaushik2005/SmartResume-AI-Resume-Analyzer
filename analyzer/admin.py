from django.contrib import admin
from .models import Analysis

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("resume_name", "job_title", "match_score", "created_at")
    search_fields = ("resume_name", "job_title")
    list_filter = ("created_at",)
