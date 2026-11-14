from django.db import models

class Analysis(models.Model):
    resume_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=150, blank=True)
    match_score = models.FloatField()
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.resume_name} — {self.match_score:.1f}%"
