from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Messages
    path('messages/', views.messages_list, name='messages'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
    path('messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    
    # Projects
    path('projects/', views.project_list, name='projects'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    
    # Profile
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Skills
    path('skills/', views.skills_list, name='skills'),
    path('skills/<int:skill_id>/delete/', views.skill_delete, name='skill_delete'),
    path('skills/<int:skill_id>/edit/', views.skill_edit, name='skill_edit'),

    
   # Experience
    path('experience/', views.experience_list, name='experience'),
    path('experience/<int:exp_id>/edit/', views.experience_edit, name='experience_edit'),
    path('experience/<int:exp_id>/delete/', views.experience_delete, name='experience_delete'),
    
    # Education
    path('education/', views.education_list, name='education'),
    path('education/<int:edu_id>/edit/', views.education_edit, name='education_edit'),
    path('education/<int:edu_id>/delete/', views.education_delete, name='education_delete'),
    
    path('certifications/', views.certifications_list, name='certifications'),
    path('certifications/<int:cert_id>/edit/', views.certification_edit, name='certification_edit'),
    path('certifications/<int:cert_id>/delete/', views.certification_delete, name='certification_delete'),
    
    
    # Services
    path('services/', views.services_list, name='services'),
    # Services
path('services/', views.services_list, name='services'),
path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
path('services/<int:service_id>/delete/', views.service_delete, name='service_delete'),
    
    # Testimonials
    # Testimonials
path('testimonials/', views.testimonials_list, name='testimonials'),
path('testimonials/<int:testimonial_id>/edit/', views.testimonial_edit, name='testimonial_edit'),
path('testimonials/<int:testimonial_id>/delete/', views.testimonial_delete, name='testimonial_delete'),
    
     # Technologies
    path('technologies/', views.technologies_list, name='technologies'),
    path('technologies/<int:tech_id>/delete/', views.technology_delete, name='technology_delete'),
    
    # Settings
    path('settings/', views.site_settings, name='site_settings'),
    path('analytics/', views.analytics_view, name='analytics'),

    
    # Blog Posts
path('blog/', views.blog_posts, name='blog_posts'),
path('blog/create/', views.blog_post_create, name='blog_post_create'),
path('blog/<int:post_id>/edit/', views.blog_post_edit, name='blog_post_edit'),
path('blog/<int:post_id>/delete/', views.blog_post_delete, name='blog_post_delete'),
]