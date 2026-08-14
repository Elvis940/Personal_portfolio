

from django.shortcuts import render, get_object_or_404
from .models import Service


def service_list(request):
    """Services listing page"""
    services = Service.objects.filter(is_active=True).order_by('order')
    featured_services = services.filter(is_featured=True)
    
    context = {
        'services': services,
        'featured_services': featured_services,
    }
    return render(request, 'services/service_list.html', context)


def service_detail(request, slug):
    """Service detail page"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    context = {
        'service': service,
    }
    return render(request, 'services/service_detail.html', context)