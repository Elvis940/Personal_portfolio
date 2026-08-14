from django.shortcuts import render
from django.db.models import Count
from apps.projects.models import Project, Technology
from apps.profiles.models import Profile, Skill, Experience, Education, Certification


def home(request):
    """Home page view"""
    
    # Get profile data
    profile = Profile.objects.first()
    
    # Get featured projects
    featured_projects = Project.objects.filter(
        is_featured=True,
        is_published=True
    ).prefetch_related('technologies', 'categories')[:6]
    
    # If no featured projects, get latest published projects
    if not featured_projects:
        featured_projects = Project.objects.filter(
            is_published=True
        ).prefetch_related('technologies', 'categories')[:6]
    
    # Get all projects for statistics
    all_projects = Project.objects.filter(is_published=True)
    
    # Get skills
    featured_skills = Skill.objects.filter(is_featured=True)[:8]
    
    # Get technologies (for stats)
    technologies = Technology.objects.all()
    
    # Get experiences for preview
    recent_experiences = Experience.objects.all()[:3]
    
    # Get certifications count
    certifications_count = Certification.objects.count()
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'projects_count': all_projects.count(),
        'technologies_count': technologies.count(),
        'featured_skills': featured_skills,
        'recent_experiences': recent_experiences,
        'certifications_count': certifications_count,
        'years_experience': 5,
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
    
    # Group skills by category
    skill_categories = {}
    for skill in skills:
        if skill.category not in skill_categories:
            skill_categories[skill.category] = []
        skill_categories[skill.category].append(skill)
    
    context = {
        'profile': profile,
        'skills': skills,
        'skill_categories': skill_categories,
        'experiences': experiences,
        'educations': educations,
        'certifications': certifications,
    }
    
    return render(request, 'core/about.html', context)