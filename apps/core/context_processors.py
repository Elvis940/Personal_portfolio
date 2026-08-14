from apps.profiles.models import Profile
from .models import SiteSettings


def site_settings(request):
    """Context processor to add site settings to all templates"""
    try:
        settings = SiteSettings.get_settings()
    except:
        settings = None
    
    return {
        'site_settings': settings,
    }


def site_settings(request):
    """Context processor to add profile data to all templates"""
    try:
        profile = Profile.objects.first()
    except:
        profile = None
    
    return {
        'profile': profile,
    }