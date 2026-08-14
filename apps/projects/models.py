from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField


class Technology(models.Model):
    """Technologies used in projects"""
    
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    color = models.CharField(max_length=7, default='#6c757d', help_text="Hex color code")
    category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    """Categories for projects"""
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#0d6efd')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio projects"""
    
    class Status(models.TextChoices):
        COMPLETED = 'COMPLETED', 'Completed'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        CONCEPT = 'CONCEPT', 'Concept'
    
    # Basic Information - INCREASED FIELD LENGTHS
    title = models.CharField(max_length=200)  # Was 100
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField(max_length=20000)  # Was 200
    description = RichTextField(blank=True)
    
    # Project Details
    problem = RichTextField(blank=True, help_text="The problem this project solves")
    solution = RichTextField(blank=True, help_text="The solution approach")
    features = models.TextField(blank=True, help_text="Key features bullet points")
    challenges = models.TextField(blank=True, help_text="Challenges faced during development")
    lessons_learned = models.TextField(blank=True)
    
    # Media
    featured_image = models.ImageField(
        upload_to='projects/featured/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    screenshots = models.ImageField(
        upload_to='projects/screenshots/',
        blank=True,
        null=True
    )
    architecture_diagram = models.ImageField(
        upload_to='projects/architecture/',
        blank=True,
        null=True
    )
    
    # Links
    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True)
    
    # Organization
    categories = models.ManyToManyField(ProjectCategory, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.COMPLETED)  # Was 20
    
    # Dates
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    
    # SEO - INCREASED FIELD LENGTHS
    meta_title = models.CharField(max_length=200, blank=True)  # Was 100
    meta_description = models.CharField(max_length=300, blank=True)  # Was 200
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-is_featured', 'order', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:200]  # Truncate to new max
        if not self.meta_description:
            self.meta_description = self.summary[:300]  # Truncate to new max
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
    image = models.ImageField(
        upload_to='projects/images/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.project.title}"
