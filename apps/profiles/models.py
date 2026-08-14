from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField


class Profile(models.Model):
    """Professional profile for Elvis T. Harmon"""
    
    # Personal Information
    first_name = models.CharField(max_length=50, default='Elvis')
    last_name = models.CharField(max_length=50, default='Harmon')
    display_name = models.CharField(max_length=100, blank=True, default='Elvis T. Harmon')
    email = models.EmailField(default='harmonelvis78@gmail.com')
    phone = models.CharField(max_length=20, blank=True, default='+1 (555) 123-4567')
    location = models.CharField(max_length=100, blank=True, default='San Francisco, CA')
    
    # Hero Section Content
    hero_badge = models.CharField(max_length=100, blank=True, null=True, default='Software Engineer')
    hero_title = models.CharField(max_length=200, blank=True, null=True, default='Building Intelligent Software')
    hero_subtitle = models.CharField(max_length=200, blank=True, null=True, default='That Solves Real Problems')
    welcome_text = models.CharField(max_length=100, blank=True, null=True, default="Hello, I'm")
    
    # Professional Information
    title = models.CharField(max_length=100, blank=True, null=True, default='Senior Software Engineer')
    headline = models.CharField(max_length=200, blank=True, null=True, default='Building Intelligent Software That Solves Real Problems')
    bio = RichTextField(blank=True, null=True)
    short_bio = models.TextField(max_length=500, blank=True, null=True)
    
    # Hero Description (paragraph after typewriter)
    hero_description = models.TextField(max_length=500, blank=True, null=True, 
        default='A passionate software engineer dedicated to building innovative solutions that make a difference. Specializing in full-stack development, artificial intelligence, and creating impactful technology.')
    
    # Social Links
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    
    # Footer Content
    footer_bio = models.TextField(max_length=300, blank=True, null=True, 
        default='Building intelligent software that solves real problems.')
    footer_copyright = models.CharField(max_length=200, blank=True, null=True, default='All rights reserved.')
    
    # Footer Contact Info
    footer_email = models.EmailField(blank=True, null=True, default='harmonelvis78@gmail.com')
    footer_phone = models.CharField(max_length=20, blank=True, null=True, default='+1 (555) 123-4567')
    footer_location = models.CharField(max_length=100, blank=True, null=True, default='San Francisco, CA')
    
    # Profile Media
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    about_image = models.ImageField(
        upload_to='profiles/about/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        help_text='Square image for the about page (recommended: 400x400px or larger)'
    )
    resume_pdf = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf'])]
    )
    
    # Meta
    slug = models.SlugField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug and self.first_name and self.last_name:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        if not self.display_name:
            self.display_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.display_name
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Skill(models.Model):
    """Technical skills with proficiency levels"""
    
    class ProficiencyLevel(models.TextChoices):
        BEGINNER = 'BEGINNER', 'Beginner'
        INTERMEDIATE = 'INTERMEDIATE', 'Intermediate'
        ADVANCED = 'ADVANCED', 'Advanced'
        EXPERT = 'EXPERT', 'Expert'
    
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, blank=True)
    proficiency = models.CharField(
        max_length=20,
        choices=ProficiencyLevel.choices,
        default=ProficiencyLevel.INTERMEDIATE
    )
    years_experience = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['order', '-years_experience']
    
    def __str__(self):
        return f"{self.name} - {self.get_proficiency_display()}"


class Experience(models.Model):
    """Work experience entries"""
    
    organization = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = RichTextField(blank=True)
    responsibilities = models.TextField(blank=True)
    technologies = models.ManyToManyField('profiles.Skill', blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.position} at {self.organization}"


class Education(models.Model):
    """Education entries"""
    
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    achievements = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Certification(models.Model):
    """Professional certifications"""
    
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    certificate_image = models.ImageField(
        upload_to='certificates/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])]
    )
    is_verified = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.name} - {self.organization}"