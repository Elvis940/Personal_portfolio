from apps.profiles.models import Profile
from .models import SiteSettings


def site_settings(request):
    """
    Context processor to add site settings and profile data to all templates.
    This makes 'site_settings' and 'profile' available in every template.
    """
    context = {}
    
    # Get site settings
    try:
        settings = SiteSettings.objects.first()
        if not settings:
            # Create default settings if none exist
            settings = SiteSettings.objects.create()
        context['site_settings'] = settings
    except Exception as e:
        # If there's an error, just set to None
        context['site_settings'] = None
    
    # Get profile data
    try:
        profile = Profile.objects.first()
        context['profile'] = profile
    except Exception as e:
        context['profile'] = None
    
    return context