from django.shortcuts import render
from django.db.models import Count
from apps.projects.models import Project, Technology
from apps.profiles.models import Profile, Skill, Experience, Education, Certification
from apps.testimonials.models import Testimonial


def home(request):
    """Home page view"""
    
    # Get profile data
    profile = Profile.objects.first()
    
    # Get ALL published projects (not just featured)
    all_projects = Project.objects.filter(is_published=True)
    
    # Get featured projects for display
    featured_projects = all_projects.filter(is_featured=True)[:6]
    
    # If no featured projects, get latest published projects
    if not featured_projects:
        featured_projects = all_projects.order_by('-created_at')[:6]
    
    # Get skills
    featured_skills = Skill.objects.filter(is_featured=True)[:8]
    
    # Get technologies (for stats)
    technologies = Technology.objects.all()
    technologies_count = technologies.count()
    
    # Get experiences for preview
    recent_experiences = Experience.objects.all()[:3]
    
    # Get certifications count
    certifications_count = Certification.objects.count()
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True).order_by('order')[:4]
    if not testimonials:
        testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:4]
    
    # Get project count
    projects_count = all_projects.count()
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'projects_count': projects_count,  # This is the count displayed in stats
        'technologies_count': technologies_count,
        'featured_skills': featured_skills,
        'recent_experiences': recent_experiences,
        'certifications_count': certifications_count,
        'years_experience': 5,
        'testimonials': testimonials,
    }
    
    return render(request, 'core/home.html', context)


def about(request):
    """About page view"""
    
    # Get profile data
    profile = Profile.objects.first()
    
    # Get all profile data
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    certifications = Certification.objects.all()
    certifications_count = certifications.count()
    
    # Group skills by category
    skill_categories = {}
    for skill in skills:
        category = skill.category if skill.category else 'General'
        if category not in skill_categories:
            skill_categories[category] = []
        skill_categories[category].append(skill)
    
    context = {
        'profile': profile,
        'skills': skills,
        'skill_categories': skill_categories,
        'experiences': experiences,
        'educations': educations,
        'certifications': certifications,
        'certifications_count': certifications_count,
    }
    
    return render(request, 'core/about.html', context)


def download_cv(request):
    """Download CV from database"""
    from django.http import HttpResponse
    
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