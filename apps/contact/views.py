from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
import logging

from .forms import ContactForm
from .models import ContactMessage

logger = logging.getLogger(__name__)


@csrf_protect
@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact page view"""
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Save the message
            message = form.save(commit=False)
            message.ip_address = get_client_ip(request)
            message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            message.referrer = request.META.get('HTTP_REFERER', '')
            message.save()
            
            messages.success(
                request, 
                'Thank you for your message! I\'ll get back to you within 24 hours.'
            )
            
            return redirect('contact:success')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Contact Me',
    }
    
    return render(request, 'contact/contact.html', context)


def contact_success(request):
    """Success page after form submission"""
    return render(request, 'contact/success.html')


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip