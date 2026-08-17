from django.shortcuts import render
from django.http import HttpResponse
from apps.profiles.models import Profile


def home(request):
    """Home page view"""
    profile = Profile.objects.first()
    context = {
        'profile': profile,
        'years_experience': 5,
        'projects_count': 0,
        'technologies_count': 0,
        'certifications_count': 0,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page view"""
    profile = Profile.objects.first()
    context = {
        'profile': profile,
    }
    return render(request, 'core/about.html', context)


def download_cv(request):
    """Download CV from database"""
    profile = Profile.objects.first()
    
    if not profile:
        return HttpResponse("Profile not found", status=404)
    
    if not profile.resume_file:
        return HttpResponse("No CV uploaded", status=404)
    
    # Create response with the binary data
    response = HttpResponse(profile.resume_file, content_type='application/pdf')
    
    # Set filename for download
    filename = profile.resume_filename or "Elvis_Harmon_CV.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response