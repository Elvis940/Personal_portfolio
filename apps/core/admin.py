from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'admin_email', 'primary_color', 'maintenance_mode', 'updated_at']
    
    fieldsets = (
        ('General Settings', {
            'fields': ('site_name', 'site_tagline', 'site_description')
        }),
        ('Email Settings', {
            'fields': ('admin_email', 'default_from_email', 'email_subject_prefix')
        }),
        ('Social Media Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'youtube_url', 'facebook_url', 'instagram_url')
        }),
        ('Appearance Settings', {
            'fields': ('primary_color', 'secondary_color', 'accent_color', 'font_family', 'default_theme')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'google_analytics_id')
        }),
        ('Footer Settings', {
            'fields': ('footer_copyright', 'footer_about', 'footer_email', 'footer_phone', 'footer_location', 'footer_quick_links', 'footer_services')
        }),
        ('Advanced Settings', {
            'fields': ('site_url', 'maintenance_mode', 'maintenance_message', 'analytics_code', 'custom_css', 'custom_js', 'robots_txt'),
            'classes': ('collapse',)
        }),
    )