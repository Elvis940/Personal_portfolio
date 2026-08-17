from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core pages
    path('', include('apps.core.urls')),
    
    # Apps
    path('projects/', include('apps.projects.urls')),
    path('blog/', include('apps.blog.urls')),
    path('services/', include('apps.services.urls')),
    path('contact/', include('apps.contact.urls')),
    path('profile/', include('apps.profiles.urls')),  # This must exist!
    path('testimonials/', include('apps.testimonials.urls')),
    
    # Dashboard
    path('dashboard/', include('apps.dashboard.urls')),
    
    # Analytics
    path('analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)