from django.shortcuts import render
from django.db.models import Count
from apps.projects.models import Project, Technology
from apps.profiles.models import Profile, Skill, Experience, Education, Certification
from apps.testimonials.models import Testimonial


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
    
    # Get testimonials (featured and active)
    testimonials = Testimonial.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('order')[:4]
    
    # If no featured testimonials, get any active ones
    if not testimonials:
        testimonials = Testimonial.objects.filter(
            is_active=True
        ).order_by('order')[:4]
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'projects_count': all_projects.count(),
        'technologies_count': technologies.count(),
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