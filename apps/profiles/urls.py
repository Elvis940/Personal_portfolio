from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('download-cv/', views.download_cv, name='download_cv'),
]