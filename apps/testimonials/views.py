from django.shortcuts import render
from .models import Testimonial


def testimonial_list(request):
    """Testimonials listing page"""
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
    featured_testimonials = testimonials.filter(is_featured=True)
    
    context = {
        'testimonials': testimonials,
        'featured_testimonials': featured_testimonials,
    }
    return render(request, 'testimonials/testimonial_list.html', context)