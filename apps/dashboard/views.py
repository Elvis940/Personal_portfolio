from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.conf import settings
import os

# Import all models
from apps.contact.models import ContactMessage
from apps.projects.models import Project, ProjectCategory, Technology
from apps.blog.models import BlogPost, BlogCategory, BlogTag
from apps.profiles.models import Profile, Skill, Experience, Education, Certification
from apps.services.models import Service
from apps.testimonials.models import Testimonial
from apps.analytics.models import AnalyticsEvent
from apps.core.models import SiteSettings



def admin_login(request):
    """Custom admin login page"""
    if request.session.get('admin_logged_in'):
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email == "harmonelvis78@gmail.com" and password == "Godiswilling231@":
            request.session['admin_logged_in'] = True
            request.session['admin_email'] = email
            messages.success(request, 'Welcome back, Elvis!')
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    
    return render(request, 'dashboard/login.html')


def admin_logout(request):
    """Logout from admin dashboard"""
    request.session.flush()
    messages.info(request, 'You have been logged out.')
    return redirect('dashboard:login')


def check_login(view_func):
    """Decorator to check if admin is logged in"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            messages.error(request, 'Please login to access the dashboard.')
            return redirect('dashboard:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@check_login
def dashboard(request):
    """Main admin dashboard"""
    
    total_messages = ContactMessage.objects.count()
    new_messages = ContactMessage.objects.filter(status='NEW').count()
    contacted_messages = ContactMessage.objects.filter(status='CONTACTED').count()
    in_discussion = ContactMessage.objects.filter(status='IN_DISCUSSION').count()
    completed_messages = ContactMessage.objects.filter(status='COMPLETED').count()
    
    recent_messages = ContactMessage.objects.order_by('-created_at')[:10]
    
    week_ago = timezone.now() - timedelta(days=7)
    weekly_messages = ContactMessage.objects.filter(created_at__gte=week_ago).count()
    weekly_new = ContactMessage.objects.filter(created_at__gte=week_ago, status='NEW').count()
    
    total_projects = Project.objects.count()
    published_projects = Project.objects.filter(is_published=True).count()
    featured_projects = Project.objects.filter(is_featured=True).count()
    
    total_blog_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(is_published=True).count()
    
    total_testimonials = Testimonial.objects.count()
    featured_testimonials = Testimonial.objects.filter(is_featured=True, is_active=True).count()
    
    total_services = Service.objects.count()
    active_services = Service.objects.filter(is_active=True).count()
    
    total_skills = Skill.objects.count()
    featured_skills = Skill.objects.filter(is_featured=True).count()
    
    total_experience = Experience.objects.count()
    current_experience = Experience.objects.filter(is_current=True).count()
    
    total_education = Education.objects.count()
    completed_education = Education.objects.filter(is_current=False).count()
    
    total_certifications = Certification.objects.count()
    verified_certifications = Certification.objects.filter(is_verified=True).count()
    
    context = {
        'total_messages': total_messages,
        'new_messages': new_messages,
        'new_messages_count': new_messages,
        'contacted_messages': contacted_messages,
        'in_discussion': in_discussion,
        'completed_messages': completed_messages,
        'recent_messages': recent_messages,
        'weekly_messages': weekly_messages,
        'weekly_new': weekly_new,
        'total_projects': total_projects,
        'published_projects': published_projects,
        'featured_projects': featured_projects,
        'total_blog_posts': total_blog_posts,
        'published_posts': published_posts,
        'total_testimonials': total_testimonials,
        'featured_testimonials': featured_testimonials,
        'total_services': total_services,
        'active_services': active_services,
        'total_skills': total_skills,
        'featured_skills': featured_skills,
        'total_experience': total_experience,
        'current_experience': current_experience,
        'total_education': total_education,
        'completed_education': completed_education,
        'total_certifications': total_certifications,
        'verified_certifications': verified_certifications,
        'admin_email': request.session.get('admin_email', 'harmonelvis78@gmail.com'),
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@check_login
def messages_list(request):
    """View all contact messages"""
    status_filter = request.GET.get('status')
    search_query = request.GET.get('search')
    
    messages_queryset = ContactMessage.objects.all()
    
    if status_filter:
        messages_queryset = messages_queryset.filter(status=status_filter)
    
    if search_query:
        messages_queryset = messages_queryset.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    messages_queryset = messages_queryset.order_by('-created_at')
    
    paginator = Paginator(messages_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    status_counts = ContactMessage.objects.values('status').annotate(count=Count('id'))
    status_count_dict = {item['status']: item['count'] for item in status_counts}
    
    context = {
        'messages': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_counts': status_count_dict,
        'status_choices': ContactMessage.Status.choices,
        'is_paginated': page_obj.has_other_pages(),
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    
    return render(request, 'dashboard/messages.html', context)


@check_login
def message_detail(request, message_id):
    """View individual message details"""
    message = get_object_or_404(ContactMessage, id=message_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes')
        
        if new_status in dict(ContactMessage.Status.choices):
            old_status = message.status
            message.status = new_status
            if new_status == 'CONTACTED' and not message.contacted_at:
                message.contacted_at = timezone.now()
            message.notes = notes
            message.save()
            
            messages.success(request, f'Message status updated to {message.get_status_display()}')
        
        return redirect('dashboard:message_detail', message_id=message_id)
    
    context = {
        'message': message,
        'status_choices': ContactMessage.Status.choices,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    
    return render(request, 'dashboard/message_detail.html', context)


@check_login
def delete_message(request, message_id):
    """Delete a message"""
    if request.method == 'POST':
        message = get_object_or_404(ContactMessage, id=message_id)
        message.delete()
        messages.success(request, 'Message deleted successfully.')
    return redirect('dashboard:messages')


@check_login
def project_list(request):
    """Manage projects"""
    projects = Project.objects.all().order_by('-created_at')
    
    context = {
        'projects': projects,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/projects.html', context)


@check_login
def project_create(request):
    """Create a new project"""
    if request.method == 'POST':
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        description = request.POST.get('description')
        status = request.POST.get('status')
        is_featured = request.POST.get('is_featured') == 'on'
        is_published = request.POST.get('is_published') == 'on'
        github_url = request.POST.get('github_url')
        live_demo_url = request.POST.get('live_demo_url')
        problem = request.POST.get('problem')
        solution = request.POST.get('solution')
        features = request.POST.get('features')
        challenges = request.POST.get('challenges')
        lessons_learned = request.POST.get('lessons_learned')
        
        project = Project.objects.create(
            title=title,
            summary=summary,
            description=description,
            status=status,
            is_featured=is_featured,
            is_published=is_published,
            github_url=github_url,
            live_demo_url=live_demo_url,
            problem=problem,
            solution=solution,
            features=features,
            challenges=challenges,
            lessons_learned=lessons_learned,
        )
        
        if request.FILES.get('featured_image'):
            project.featured_image = request.FILES.get('featured_image')
            project.save()
        
        category_ids = request.POST.getlist('categories')
        if category_ids:
            project.categories.set(category_ids)
        
        tech_ids = request.POST.getlist('technologies')
        if tech_ids:
            project.technologies.set(tech_ids)
        
        messages.success(request, f'Project "{title}" created successfully!')
        return redirect('dashboard:projects')
    
    categories = ProjectCategory.objects.all()
    technologies = Technology.objects.all()
    
    context = {
        'categories': categories,
        'technologies': technologies,
        'status_choices': Project.Status.choices,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/project_form.html', context)


@check_login
def project_edit(request, project_id):
    """Edit a project"""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.summary = request.POST.get('summary')
        project.description = request.POST.get('description')
        project.status = request.POST.get('status')
        project.is_featured = request.POST.get('is_featured') == 'on'
        project.is_published = request.POST.get('is_published') == 'on'
        project.github_url = request.POST.get('github_url')
        project.live_demo_url = request.POST.get('live_demo_url')
        project.problem = request.POST.get('problem')
        project.solution = request.POST.get('solution')
        project.features = request.POST.get('features')
        project.challenges = request.POST.get('challenges')
        project.lessons_learned = request.POST.get('lessons_learned')
        
        if request.FILES.get('featured_image'):
            project.featured_image = request.FILES.get('featured_image')
            project.save()
        
        category_ids = request.POST.getlist('categories')
        if category_ids:
            project.categories.set(category_ids)
        
        tech_ids = request.POST.getlist('technologies')
        if tech_ids:
            project.technologies.set(tech_ids)
        
        messages.success(request, f'Project "{project.title}" updated successfully!')
        return redirect('dashboard:projects')
    
    categories = ProjectCategory.objects.all()
    technologies = Technology.objects.all()
    
    context = {
        'project': project,
        'categories': categories,
        'technologies': technologies,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/project_edit.html', context)


@check_login
def project_delete(request, project_id):
    """Delete a project"""
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project_title = project.title
        project.delete()
        messages.success(request, f'Project "{project_title}" deleted successfully!')
    return redirect('dashboard:projects')


@check_login
def profile_edit(request):
    """Edit profile"""
    profile = Profile.objects.first()
    
    if request.method == 'POST':
        if not profile:
            profile = Profile()
        
        # Personal Information
        profile.first_name = request.POST.get('first_name', 'Elvis')
        profile.last_name = request.POST.get('last_name', 'Harmon')
        profile.email = request.POST.get('email', 'harmonelvis78@gmail.com')
        profile.phone = request.POST.get('phone', '+1 (555) 123-4567')
        profile.location = request.POST.get('location', 'San Francisco, CA')
        profile.display_name = request.POST.get('display_name', f"{profile.first_name} {profile.last_name}")
        
        # Hero Section
        profile.hero_badge = request.POST.get('hero_badge', 'Software Engineer')
        profile.hero_title = request.POST.get('hero_title', 'Building Intelligent Software')
        profile.hero_subtitle = request.POST.get('hero_subtitle', 'That Solves Real Problems')
        profile.welcome_text = request.POST.get('welcome_text', "Hello, I'm")
        profile.hero_description = request.POST.get('hero_description', 
            'A passionate software engineer dedicated to building innovative solutions that make a difference.')
        
        # Professional Information
        profile.title = request.POST.get('title', 'Senior Software Engineer')
        profile.headline = request.POST.get('headline', 'Building Intelligent Software That Solves Real Problems')
        profile.bio = request.POST.get('bio', '')
        profile.short_bio = request.POST.get('short_bio', '')
        
        # Social Links
        profile.github_url = request.POST.get('github_url', '')
        profile.linkedin_url = request.POST.get('linkedin_url', '')
        profile.twitter_url = request.POST.get('twitter_url', '')
        profile.youtube_url = request.POST.get('youtube_url', '')
        
        # Footer Content
        profile.footer_bio = request.POST.get('footer_bio', 'Building intelligent software that solves real problems.')
        profile.footer_copyright = request.POST.get('footer_copyright', 'All rights reserved.')
        profile.footer_email = request.POST.get('footer_email', 'harmonelvis78@gmail.com')
        profile.footer_phone = request.POST.get('footer_phone', '+1 (555) 123-4567')
        profile.footer_location = request.POST.get('footer_location', 'San Francisco, CA')
        
        # Profile Images
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES.get('profile_image')
        if request.FILES.get('about_image'):
            profile.about_image = request.FILES.get('about_image')
        
        # Resume Upload - Read the file and store in BinaryField
        if request.FILES.get('resume_pdf'):
            resume_file = request.FILES.get('resume_pdf')
            # Read the file content as bytes
            profile.resume_file = resume_file.read()
            profile.resume_filename = resume_file.name
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard:profile_edit')
    
    context = {
        'profile': profile,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/profile_edit.html', context)


@check_login
def skills_list(request):
    """Manage skills"""
    skills = Skill.objects.all().order_by('category', 'order')
    categories = Skill.objects.values_list('category', flat=True).distinct()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        proficiency = request.POST.get('proficiency')
        years_experience = request.POST.get('years_experience', 0)
        is_featured = request.POST.get('is_featured') == 'on'
        icon = request.POST.get('icon', '')
        order = request.POST.get('order', 0)
        
        Skill.objects.create(
            name=name,
            category=category,
            proficiency=proficiency,
            years_experience=years_experience,
            is_featured=is_featured,
            icon=icon,
            order=order
        )
        messages.success(request, f'Skill "{name}" added successfully!')
        return redirect('dashboard:skills')
    
    context = {
        'skills': skills,
        'categories': categories,
        'proficiency_choices': Skill.ProficiencyLevel.choices,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/skills.html', context)


@check_login
def skill_edit(request, skill_id):
    """Edit a skill"""
    skill = get_object_or_404(Skill, id=skill_id)
    
    if request.method == 'POST':
        skill.name = request.POST.get('name')
        skill.category = request.POST.get('category')
        skill.proficiency = request.POST.get('proficiency')
        skill.years_experience = request.POST.get('years_experience', 0)
        skill.is_featured = request.POST.get('is_featured') == 'on'
        skill.icon = request.POST.get('icon', '')
        skill.order = request.POST.get('order', 0)
        skill.save()
        
        messages.success(request, f'Skill "{skill.name}" updated successfully!')
        return redirect('dashboard:skills')
    
    context = {
        'skill': skill,
        'proficiency_choices': Skill.ProficiencyLevel.choices,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/skill_edit.html', context)


@check_login
def skill_delete(request, skill_id):
    """Delete a skill"""
    if request.method == 'POST':
        skill = get_object_or_404(Skill, id=skill_id)
        skill_name = skill.name
        skill.delete()
        messages.success(request, f'Skill "{skill_name}" deleted successfully!')
    return redirect('dashboard:skills')


@check_login
def experience_list(request):
    """Manage experience entries"""
    experiences = Experience.objects.all().order_by('-start_date')
    
    if request.method == 'POST':
        organization = request.POST.get('organization')
        position = request.POST.get('position')
        location = request.POST.get('location')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_current = request.POST.get('is_current') == 'on'
        description = request.POST.get('description')
        responsibilities = request.POST.get('responsibilities')
        
        Experience.objects.create(
            organization=organization,
            position=position,
            location=location,
            start_date=start_date,
            end_date=end_date if end_date else None,
            is_current=is_current,
            description=description,
            responsibilities=responsibilities
        )
        messages.success(request, f'Experience at "{organization}" added successfully!')
        return redirect('dashboard:experience')
    
    context = {
        'experiences': experiences,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/experience.html', context)


@check_login
def experience_edit(request, exp_id):
    """Edit an experience entry"""
    exp = get_object_or_404(Experience, id=exp_id)
    
    if request.method == 'POST':
        exp.organization = request.POST.get('organization')
        exp.position = request.POST.get('position')
        exp.location = request.POST.get('location')
        exp.start_date = request.POST.get('start_date')
        exp.end_date = request.POST.get('end_date') if request.POST.get('end_date') else None
        exp.is_current = request.POST.get('is_current') == 'on'
        exp.description = request.POST.get('description')
        exp.responsibilities = request.POST.get('responsibilities')
        exp.save()
        
        messages.success(request, f'Experience at "{exp.organization}" updated successfully!')
        return redirect('dashboard:experience')
    
    context = {
        'experience': exp,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/experience_edit.html', context)


@check_login
def experience_delete(request, exp_id):
    """Delete an experience entry"""
    if request.method == 'POST':
        exp = get_object_or_404(Experience, id=exp_id)
        org_name = exp.organization
        exp.delete()
        messages.success(request, f'Experience at "{org_name}" deleted successfully!')
    return redirect('dashboard:experience')


@check_login
def education_list(request):
    """Manage education entries"""
    educations = Education.objects.all().order_by('-start_date')
    
    if request.method == 'POST':
        institution = request.POST.get('institution')
        degree = request.POST.get('degree')
        field_of_study = request.POST.get('field_of_study')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_current = request.POST.get('is_current') == 'on'
        gpa = request.POST.get('gpa')
        achievements = request.POST.get('achievements')
        
        Education.objects.create(
            institution=institution,
            degree=degree,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date if end_date else None,
            is_current=is_current,
            gpa=gpa if gpa else None,
            achievements=achievements
        )
        messages.success(request, f'Education at "{institution}" added successfully!')
        return redirect('dashboard:education')
    
    context = {
        'educations': educations,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/education.html', context)


@check_login
def education_edit(request, edu_id):
    """Edit an education entry"""
    edu = get_object_or_404(Education, id=edu_id)
    
    if request.method == 'POST':
        edu.institution = request.POST.get('institution')
        edu.degree = request.POST.get('degree')
        edu.field_of_study = request.POST.get('field_of_study')
        edu.start_date = request.POST.get('start_date')
        edu.end_date = request.POST.get('end_date') if request.POST.get('end_date') else None
        edu.is_current = request.POST.get('is_current') == 'on'
        edu.gpa = request.POST.get('gpa') if request.POST.get('gpa') else None
        edu.achievements = request.POST.get('achievements')
        edu.save()
        
        messages.success(request, f'Education at "{edu.institution}" updated successfully!')
        return redirect('dashboard:education')
    
    context = {
        'education': edu,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/education_edit.html', context)


@check_login
def education_delete(request, edu_id):
    """Delete an education entry"""
    if request.method == 'POST':
        edu = get_object_or_404(Education, id=edu_id)
        inst_name = edu.institution
        edu.delete()
        messages.success(request, f'Education at "{inst_name}" deleted successfully!')
    return redirect('dashboard:education')


@check_login
def certifications_list(request):
    """Manage certifications"""
    certifications = Certification.objects.all().order_by('-issue_date')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        organization = request.POST.get('organization')
        issue_date = request.POST.get('issue_date')
        expiry_date = request.POST.get('expiry_date')
        credential_id = request.POST.get('credential_id')
        credential_url = request.POST.get('credential_url')
        is_verified = request.POST.get('is_verified') == 'on'
        
        cert = Certification.objects.create(
            name=name,
            organization=organization,
            issue_date=issue_date,
            expiry_date=expiry_date if expiry_date else None,
            credential_id=credential_id,
            credential_url=credential_url,
            is_verified=is_verified
        )
        
        if request.FILES.get('certificate_image'):
            cert.certificate_image = request.FILES.get('certificate_image')
            cert.save()
        
        messages.success(request, f'Certification "{name}" added successfully!')
        return redirect('dashboard:certifications')
    
    context = {
        'certifications': certifications,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/certifications.html', context)


@check_login
def certification_edit(request, cert_id):
    """Edit a certification"""
    cert = get_object_or_404(Certification, id=cert_id)
    
    if request.method == 'POST':
        cert.name = request.POST.get('name')
        cert.organization = request.POST.get('organization')
        cert.issue_date = request.POST.get('issue_date')
        cert.expiry_date = request.POST.get('expiry_date') if request.POST.get('expiry_date') else None
        cert.credential_id = request.POST.get('credential_id')
        cert.credential_url = request.POST.get('credential_url')
        cert.is_verified = request.POST.get('is_verified') == 'on'
        
        if request.FILES.get('certificate_image'):
            cert.certificate_image = request.FILES.get('certificate_image')
        
        cert.save()
        messages.success(request, f'Certification "{cert.name}" updated successfully!')
        return redirect('dashboard:certifications')
    
    context = {
        'certification': cert,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/certification_edit.html', context)


@check_login
def certification_delete(request, cert_id):
    """Delete a certification"""
    if request.method == 'POST':
        cert = get_object_or_404(Certification, id=cert_id)
        cert_name = cert.name
        cert.delete()
        messages.success(request, f'Certification "{cert_name}" deleted successfully!')
    return redirect('dashboard:certifications')


@check_login
def services_list(request):
    """Manage services"""
    services = Service.objects.all().order_by('order')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        features = request.POST.get('features')
        technologies = request.POST.get('technologies')
        icon = request.POST.get('icon')
        is_active = request.POST.get('is_active') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        order = request.POST.get('order', 0)
        
        service = Service.objects.create(
            name=name,
            description=description,
            features=features,
            technologies=technologies,
            icon=icon,
            is_active=is_active,
            is_featured=is_featured,
            order=order
        )
        
        if request.FILES.get('image'):
            service.image = request.FILES.get('image')
            service.save()
        
        messages.success(request, f'Service "{name}" added successfully!')
        return redirect('dashboard:services')
    
    context = {
        'services': services,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/services.html', context)


@check_login
def service_edit(request, service_id):
    """Edit a service"""
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.features = request.POST.get('features')
        service.technologies = request.POST.get('technologies')
        service.icon = request.POST.get('icon')
        service.is_active = request.POST.get('is_active') == 'on'
        service.is_featured = request.POST.get('is_featured') == 'on'
        service.order = request.POST.get('order', 0)
        
        if request.FILES.get('image'):
            service.image = request.FILES.get('image')
        
        service.save()
        messages.success(request, f'Service "{service.name}" updated successfully!')
        return redirect('dashboard:services')
    
    context = {
        'service': service,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/service_edit.html', context)


@check_login
def service_delete(request, service_id):
    """Delete a service"""
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        service_name = service.name
        service.delete()
        messages.success(request, f'Service "{service_name}" deleted successfully!')
    return redirect('dashboard:services')


@check_login
def testimonials_list(request):
    """Manage testimonials"""
    testimonials = Testimonial.objects.all().order_by('order')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        company = request.POST.get('company')
        content = request.POST.get('content')
        rating = request.POST.get('rating', 5)
        is_active = request.POST.get('is_active') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        order = request.POST.get('order', 0)
        
        testimonial = Testimonial.objects.create(
            name=name,
            position=position,
            company=company,
            content=content,
            rating=rating,
            is_active=is_active,
            is_featured=is_featured,
            order=order
        )
        
        if request.FILES.get('image'):
            testimonial.image = request.FILES.get('image')
            testimonial.save()
        
        messages.success(request, f'Testimonial from "{name}" added successfully!')
        return redirect('dashboard:testimonials')
    
    context = {
        'testimonials': testimonials,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/testimonials.html', context)


@check_login
def testimonial_edit(request, testimonial_id):
    """Edit a testimonial"""
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    
    if request.method == 'POST':
        testimonial.name = request.POST.get('name')
        testimonial.position = request.POST.get('position')
        testimonial.company = request.POST.get('company')
        testimonial.content = request.POST.get('content')
        testimonial.rating = request.POST.get('rating', 5)
        testimonial.is_active = request.POST.get('is_active') == 'on'
        testimonial.is_featured = request.POST.get('is_featured') == 'on'
        testimonial.order = request.POST.get('order', 0)
        
        if request.FILES.get('image'):
            testimonial.image = request.FILES.get('image')
        
        testimonial.save()
        messages.success(request, f'Testimonial from "{testimonial.name}" updated successfully!')
        return redirect('dashboard:testimonials')
    
    context = {
        'testimonial': testimonial,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/testimonial_edit.html', context)


@check_login
def testimonial_delete(request, testimonial_id):
    """Delete a testimonial"""
    if request.method == 'POST':
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
        testimonial_name = testimonial.name
        testimonial.delete()
        messages.success(request, f'Testimonial from "{testimonial_name}" deleted successfully!')
    return redirect('dashboard:testimonials')


@check_login
def technologies_list(request):
    """Manage technologies"""
    technologies = Technology.objects.all().order_by('name')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        color = request.POST.get('color', '#6C63FF')
        icon = request.POST.get('icon')
        
        Technology.objects.create(
            name=name,
            category=category,
            color=color,
            icon=icon
        )
        messages.success(request, f'Technology "{name}" added successfully!')
        return redirect('dashboard:technologies')
    
    context = {
        'technologies': technologies,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/technologies.html', context)


@check_login
def technology_delete(request, tech_id):
    """Delete a technology"""
    if request.method == 'POST':
        tech = get_object_or_404(Technology, id=tech_id)
        tech_name = tech.name
        tech.delete()
        messages.success(request, f'Technology "{tech_name}" deleted successfully!')
    return redirect('dashboard:technologies')


@check_login
def site_settings(request):
    """Site settings management"""
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        settings.site_name = request.POST.get('site_name')
        settings.site_tagline = request.POST.get('site_tagline')
        settings.site_description = request.POST.get('site_description')
        
        settings.admin_email = request.POST.get('admin_email')
        settings.default_from_email = request.POST.get('default_from_email')
        settings.email_subject_prefix = request.POST.get('email_subject_prefix')
        
        settings.github_url = request.POST.get('github_url')
        settings.linkedin_url = request.POST.get('linkedin_url')
        settings.twitter_url = request.POST.get('twitter_url')
        settings.youtube_url = request.POST.get('youtube_url')
        settings.facebook_url = request.POST.get('facebook_url')
        settings.instagram_url = request.POST.get('instagram_url')
        
        settings.primary_color = request.POST.get('primary_color')
        settings.secondary_color = request.POST.get('secondary_color')
        settings.accent_color = request.POST.get('accent_color')
        settings.font_family = request.POST.get('font_family')
        settings.default_theme = request.POST.get('default_theme')
        
        settings.meta_title = request.POST.get('meta_title')
        settings.meta_description = request.POST.get('meta_description')
        settings.meta_keywords = request.POST.get('meta_keywords')
        settings.google_analytics_id = request.POST.get('google_analytics_id')
        
        settings.footer_copyright = request.POST.get('footer_copyright')
        settings.footer_about = request.POST.get('footer_about')
        settings.footer_email = request.POST.get('footer_email')
        settings.footer_phone = request.POST.get('footer_phone')
        settings.footer_location = request.POST.get('footer_location')
        settings.footer_quick_links = request.POST.get('footer_quick_links')
        settings.footer_services = request.POST.get('footer_services')
        
        settings.site_url = request.POST.get('site_url')
        settings.maintenance_mode = request.POST.get('maintenance_mode') == 'on'
        settings.maintenance_message = request.POST.get('maintenance_message')
        settings.analytics_code = request.POST.get('analytics_code')
        settings.custom_css = request.POST.get('custom_css')
        settings.custom_js = request.POST.get('custom_js')
        settings.robots_txt = request.POST.get('robots_txt')
        
        settings.save()
        messages.success(request, 'Site settings updated successfully!')
        return redirect('dashboard:site_settings')
    
    context = {
        'settings': settings,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/site_settings.html', context)


@check_login
def analytics_view(request):
    context = {'new_messages_count': ContactMessage.objects.filter(status='NEW').count()}
    return render(request, 'dashboard/analytics.html', context)


@check_login
def blog_posts(request):
    """Manage blog posts"""
    posts = BlogPost.objects.all().order_by('-created_at')
    
    context = {
        'posts': posts,
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
    }
    return render(request, 'dashboard/blog_posts.html', context)


@check_login
def blog_post_create(request):
    """Create a new blog post"""
    if request.method == 'POST':
        title = request.POST.get('title')
        excerpt = request.POST.get('excerpt')
        content = request.POST.get('content')
        is_published = request.POST.get('is_published') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        categories = request.POST.getlist('categories')
        tags = request.POST.getlist('tags')
        
        post = BlogPost.objects.create(
            title=title,
            excerpt=excerpt,
            content=content,
            is_published=is_published,
            is_featured=is_featured,
        )
        
        if request.FILES.get('featured_image'):
            post.featured_image = request.FILES.get('featured_image')
            post.save()
        
        if categories:
            post.categories.set(categories)
        
        if tags:
            post.tags.set(tags)
        
        messages.success(request, f'Blog post "{post.title}" created successfully!')
        return redirect('dashboard:blog_posts')
    
    context = {
        'categories': BlogCategory.objects.all(),
        'tags': BlogTag.objects.all(),
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
        'is_editing': False,
    }
    return render(request, 'dashboard/blog_post_form.html', context)


@check_login
def blog_post_edit(request, post_id):
    """Edit a blog post"""
    post = get_object_or_404(BlogPost, id=post_id)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.excerpt = request.POST.get('excerpt')
        post.content = request.POST.get('content')
        post.is_published = request.POST.get('is_published') == 'on'
        post.is_featured = request.POST.get('is_featured') == 'on'
        
        if request.FILES.get('featured_image'):
            post.featured_image = request.FILES.get('featured_image')
        
        post.save()
        
        categories = request.POST.getlist('categories')
        if categories:
            post.categories.set(categories)
        else:
            post.categories.clear()
        
        tags = request.POST.getlist('tags')
        if tags:
            post.tags.set(tags)
        else:
            post.tags.clear()
        
        messages.success(request, f'Blog post "{post.title}" updated successfully!')
        return redirect('dashboard:blog_posts')
    
    context = {
        'post': post,
        'categories': BlogCategory.objects.all(),
        'tags': BlogTag.objects.all(),
        'new_messages_count': ContactMessage.objects.filter(status='NEW').count(),
        'is_editing': True,
    }
    return render(request, 'dashboard/blog_post_form.html', context)


@check_login
def blog_post_delete(request, post_id):
    """Delete a blog post"""
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, id=post_id)
        post_title = post.title
        post.delete()
        messages.success(request, f'Blog post "{post_title}" deleted successfully!')
    return redirect('dashboard:blog_posts')