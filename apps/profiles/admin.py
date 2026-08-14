from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Skill, Experience, Education, Certification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'title', 'email', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'display_name', 'email', 'phone', 'location')
        }),
        ('Hero Section Content', {
            'fields': ('hero_badge', 'hero_title', 'hero_subtitle', 'welcome_text', 'hero_description'),
            'classes': ('wide',),
            'description': 'Content displayed in the hero section of the homepage'
        }),
        ('Professional Information', {
            'fields': ('title', 'headline', 'bio', 'short_bio')
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'youtube_url', 'website_url')
        }),
        ('Footer Content', {
            'fields': ('footer_bio', 'footer_copyright', 'footer_email', 'footer_phone', 'footer_location'),
            'description': 'Content displayed in the footer'
        }),
        ('Media', {
            'fields': ('profile_image', 'resume_pdf')
        }),
        ('Meta', {
            'fields': ('slug', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'years_experience', 'is_featured']
    list_filter = ['category', 'proficiency', 'is_featured']
    search_fields = ['name']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['organization', 'position', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'technologies']
    search_fields = ['organization', 'position']
    filter_horizontal = ['technologies']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date']
    search_fields = ['institution', 'degree', 'field_of_study']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'issue_date', 'expiry_date', 'is_verified']
    search_fields = ['name', 'organization']