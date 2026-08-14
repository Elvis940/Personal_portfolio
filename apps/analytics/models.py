from django.db import models
from django.utils import timezone


class AnalyticsEvent(models.Model):
    """Analytics tracking events"""
    
    class EventType(models.TextChoices):
        PAGE_VIEW = 'page_view', 'Page View'
        PROJECT_VIEW = 'project_view', 'Project View'
        BLOG_VIEW = 'blog_view', 'Blog View'
        CV_DOWNLOAD = 'cv_download', 'CV Download'
        CONTACT_SUBMISSION = 'contact_submission', 'Contact Submission'
        SEARCH = 'search', 'Search'
    
    event_type = models.CharField(max_length=100, choices=EventType.choices)
    url = models.CharField(max_length=2000)
    referrer = models.URLField(blank=True, null=True, max_length=2000)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    session_id = models.CharField(max_length=500, blank=True, null=True)
    device_type = models.CharField(max_length=100, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    os = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Analytics Event"
        verbose_name_plural = "Analytics Events"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['url']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.url}"


class AnalyticsSummary(models.Model):
    """Daily summary of analytics data"""
    
    date = models.DateField(unique=True)
    page_views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    project_views = models.PositiveIntegerField(default=0)
    blog_views = models.PositiveIntegerField(default=0)
    cv_downloads = models.PositiveIntegerField(default=0)
    contact_submissions = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Analytics Summary"
        verbose_name_plural = "Analytics Summaries"
        ordering = ['-date']
    
    def __str__(self):
        return f"Summary for {self.date}"