from django.db import models
from ckeditor.fields import RichTextField


class SiteSettings(models.Model):
    """Site-wide settings for the portfolio"""
    
    # General Settings
    site_name = models.CharField(max_length=100, default='Elvis T. Harmon')
    site_tagline = models.CharField(max_length=200, default='Building Intelligent Software That Solves Real Problems')
    site_description = models.TextField(default='Professional portfolio of Elvis T. Harmon, a software engineer specializing in Django, Python, AI/ML, and full-stack development.')
    
    # Email Settings
    admin_email = models.EmailField(default='harmonelvis78@gmail.com')
    default_from_email = models.EmailField(default='noreply@elvisportfolio.com')
    email_subject_prefix = models.CharField(max_length=50, default='[Contact Form] ')
    
    # Social Media Links
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    
    # Appearance Settings
    primary_color = models.CharField(max_length=7, default='#6C63FF', help_text='Hex color code')
    secondary_color = models.CharField(max_length=7, default='#3F3D9E', help_text='Hex color code')
    accent_color = models.CharField(max_length=7, default='#FF6B6B', help_text='Hex color code')
    font_family = models.CharField(max_length=100, default='Inter', help_text='Google Font name')
    default_theme = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    
    # SEO Settings
    meta_title = models.CharField(max_length=100, default='Elvis T. Harmon - Software Engineer')
    meta_description = models.CharField(max_length=200, default='Building intelligent software that solves real problems. Software Engineer specializing in Django, Python, AI/ML, and full-stack development.')
    meta_keywords = models.CharField(max_length=200, blank=True, default='Software Engineer, Django, Python, AI/ML, Full-Stack Developer, Web Development')
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Footer Settings
    footer_copyright = models.CharField(max_length=200, default='© 2024 Elvis T. Harmon. All rights reserved.')
    footer_about = models.TextField(default='Building intelligent software that solves real problems.')
    footer_email = models.EmailField(default='harmonelvis78@gmail.com')
    footer_phone = models.CharField(max_length=20, default='+1 (555) 123-4567')
    footer_location = models.CharField(max_length=100, default='San Francisco, CA')
    footer_quick_links = models.TextField(blank=True, help_text='Comma separated links (e.g., Home, About, Projects, Blog)')
    footer_services = models.TextField(blank=True, help_text='Comma separated services (e.g., Web Development, Django, AI/ML)')
    
    # Advanced Settings
    site_url = models.URLField(blank=True, null=True, help_text='Your live site URL')
    maintenance_mode = models.BooleanField(default=False, help_text='Enable maintenance mode')
    maintenance_message = models.TextField(blank=True, null=True, default='We are currently undergoing maintenance. Please check back soon.')
    analytics_code = models.TextField(blank=True, null=True, help_text='Custom analytics code (e.g., Google Analytics, Facebook Pixel)')
    custom_css = models.TextField(blank=True, null=True, help_text='Custom CSS to override styles')
    custom_js = models.TextField(blank=True, null=True, help_text='Custom JavaScript to add to the site')
    robots_txt = models.TextField(blank=True, null=True, default='User-agent: *\nAllow: /')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            # If there's already a settings instance, update it instead of creating new
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get the site settings instance, create if doesn't exist"""
        settings = cls.objects.first()
        if not settings:
            settings = cls.objects.create()
        return settings