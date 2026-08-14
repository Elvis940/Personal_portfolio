from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core pages
    path('', include('apps.core.urls')),
    
    # Apps
    path('projects/', include('apps.projects.urls')),
    path('blog/', include('apps.blog.urls')),
    path('services/', include('apps.services.urls')),
    path('contact/', include('apps.contact.urls')),
    path('profile/', include('apps.profiles.urls')),
    path('testimonials/', include('apps.testimonials.urls')),
    
    # Dashboard (custom admin)
    path('dashboard/', include('apps.dashboard.urls')),
    path('analytics/', include('apps.analytics.urls')),  # Make sure this exists
    
    
    # Robots.txt
    path('robots.txt', lambda request: HttpResponse(
        "User-agent: *\nDisallow: /admin/\nDisallow: /dashboard/\nSitemap: /sitemap.xml",
        content_type="text/plain"
    )),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)