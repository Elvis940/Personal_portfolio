from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json

from .models import AnalyticsEvent


def analytics_dashboard(request):
    """Analytics dashboard view"""
    
    # Get period filter
    period = request.GET.get('period', 'month')
    today = timezone.now().date()
    
    # Set date range
    if period == 'today':
        start_date = today
    elif period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'month':
        start_date = today - timedelta(days=30)
    elif period == 'year':
        start_date = today - timedelta(days=365)
    else:
        start_date = today - timedelta(days=30)
    
    # Get events
    events = AnalyticsEvent.objects.filter(created_at__date__gte=start_date)
    
    # Stats
    total_views = events.count()
    unique_visitors = events.values('ip_address').distinct().count()
    
    # Count by event type
    page_views = events.filter(event_type='page_view').count()
    project_views = events.filter(event_type='project_view').count()
    blog_views = events.filter(event_type='blog_view').count()
    cv_downloads = events.filter(event_type='cv_download').count()
    contact_submissions = events.filter(event_type='contact_submission').count()
    
    # Event breakdown for display
    event_breakdown = list(events.values('event_type').annotate(
        count=Count('id')
    ).order_by('-count'))
    
    # Top pages
    top_pages = list(events.values('url').annotate(
        count=Count('id')
    ).order_by('-count')[:10])
    
    # Recent activity
    recent_activity = list(events.order_by('-created_at')[:20])
    
    context = {
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'page_views': page_views,
        'project_views': project_views,
        'blog_views': blog_views,
        'cv_downloads': cv_downloads,
        'contact_submissions': contact_submissions,
        'event_breakdown': event_breakdown,
        'top_pages': top_pages,
        'recent_activity': recent_activity,
        'period': period,
        'has_data': events.count() > 0,
    }
    
    return render(request, 'analytics/dashboard.html', context)


@csrf_exempt
def track_event(request):
    """Track events via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_type = data.get('event_type')
            url = data.get('url', '/')
            
            AnalyticsEvent.objects.create(
                event_type=event_type,
                url=url,
                ip_address=request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False}, status=400)
    return JsonResponse({'success': False}, status=405)