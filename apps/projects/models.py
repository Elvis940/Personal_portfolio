from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Technology(models.Model):
    """Technologies used in projects"""
    
    name = models.CharField(max_length=1000, unique=True)
    icon = models.CharField(max_length=1000, blank=True, help_text="FontAwesome icon class")
    color = models.CharField(max_length=20, default='#6c757d', help_text="Hex color code")
    category = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    """Categories for projects"""
    
    name = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=1000, blank=True)
    color = models.CharField(max_length=20, default='#0d6efd')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:1000]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio projects"""
    
    class Status(models.TextChoices):
        COMPLETED = 'COMPLETED', 'Completed'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        CONCEPT = 'CONCEPT', 'Concept'
    
    # Basic Information
    title = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    summary = models.CharField(max_length=20000)
    description = RichTextField(blank=True)
    
    # Project Details
    problem = RichTextField(blank=True, help_text="The problem this project solves")
    solution = RichTextField(blank=True, help_text="The solution approach")
    features = models.TextField(blank=True, help_text="Key features bullet points")
    challenges = models.TextField(blank=True, help_text="Challenges faced during development")
    lessons_learned = models.TextField(blank=True)
    
    # Media - Using CloudinaryField
    featured_image = CloudinaryField('image', folder='elvis_portfolio/projects', blank=True, null=True)
    screenshots = CloudinaryField('image', folder='elvis_portfolio/screenshots', blank=True, null=True)
    architecture_diagram = CloudinaryField('image', folder='elvis_portfolio/architecture', blank=True, null=True)
    
    # Links
    github_url = models.URLField(blank=True, max_length=1000)
    live_demo_url = models.URLField(blank=True, max_length=1000)
    
    # Organization
    categories = models.ManyToManyField(ProjectCategory, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.COMPLETED)
    
    # Dates
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    
    # SEO
    meta_title = models.CharField(max_length=1000, blank=True)
    meta_description = models.CharField(max_length=2000, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-is_featured', 'order', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:1000]
        if not self.meta_title:
            self.meta_title = self.title[:1000]
        if not self.meta_description:
            self.meta_description = self.summary[:2000] if self.summary else ''
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('projects:project_detail', kwargs={'slug': self.slug})
    
    def increment_view_count(self):
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])


class ProjectImage(models.Model):
    """Additional images for projects"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', folder='elvis_portfolio/project_images', blank=True, null=True)
    caption = models.CharField(max_length=1000, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.project.title}"