from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, ProjectCategory, Technology


def project_list(request):
    """Project listing page with filtering"""
    
    projects = Project.objects.filter(is_published=True).prefetch_related(
        'technologies', 'categories'
    ).order_by('-is_featured', '-created_at')
    
    # Get filter parameters
    category_slug = request.GET.get('category')
    tech_slug = request.GET.get('tech')
    search_query = request.GET.get('q')
    
    # Apply filters
    if category_slug:
        projects = projects.filter(categories__slug=category_slug)
    
    if tech_slug:
        projects = projects.filter(technologies__name__iexact=tech_slug)
    
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Get all categories and technologies for filter UI
    categories = ProjectCategory.objects.all()
    technologies = Technology.objects.all()
    
    # Pagination
    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
        'categories': categories,
        'technologies': technologies,
        'current_category': category_slug,
        'current_tech': tech_slug,
        'search_query': search_query,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'projects/project_list.html', context)


def project_detail(request, slug):
    """Project detail page"""
    
    project = get_object_or_404(Project, slug=slug, is_published=True)
    
    # Increment view count
    project.view_count = project.view_count + 1
    project.save(update_fields=['view_count'])
    
    # Get related projects (same category)
    related_projects = Project.objects.filter(
        categories__in=project.categories.all(),
        is_published=True
    ).exclude(id=project.id).distinct()[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    
    return render(request, 'projects/project_detail.html', context)