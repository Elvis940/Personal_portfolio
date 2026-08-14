from django.utils.deprecation import MiddlewareMixin
from .models import AnalyticsEvent
from .utils import get_client_ip, get_device_info
import re


class AnalyticsMiddleware(MiddlewareMixin):
    """Middleware to track page views"""
    
    EXCLUDE_PATHS = [
        r'^/admin/',
        r'^/dashboard/',
        r'^/static/',
        r'^/media/',
        r'^/favicon.ico',
        r'^/robots.txt',
        r'^/sitemap.xml',
    ]
    
    def process_request(self, request):
        path = request.path
        for pattern in self.EXCLUDE_PATHS:
            if re.match(pattern, path):
                return None
        
        if request.method != 'GET':
            return None
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return None
        
        try:
            ip_address = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            referrer = request.META.get('HTTP_REFERER', '')
            device_info = get_device_info(user_agent)
            
            AnalyticsEvent.objects.create(
                event_type=AnalyticsEvent.EventType.PAGE_VIEW,
                url=path,
                referrer=referrer,
                ip_address=ip_address,
                user_agent=user_agent,
                session_id=request.session.session_key,
                device_type=device_info.get('device_type', 'unknown'),
                browser=device_info.get('browser', 'unknown'),
                os=device_info.get('os', 'unknown'),
            )
        except:
            pass
        
        return None