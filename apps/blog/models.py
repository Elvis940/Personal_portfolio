from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from django.utils import timezone


class BlogCategory(models.Model):
    """Blog categories"""
    
    name = models.CharField(max_length=1000, unique=True)  # Was 50
    slug = models.SlugField(max_length=1000, unique=True, blank=True)  # Was default
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:1000]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class BlogTag(models.Model):
    """Blog tags"""
    
    name = models.CharField(max_length=1000, unique=True)  # Was 50
    slug = models.SlugField(max_length=1000, unique=True, blank=True)  # Was default
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:1000]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Blog posts"""
    
    title = models.CharField(max_length=1000)  # Was 200
    slug = models.SlugField(max_length=1000, unique=True, blank=True)  # Was default
    excerpt = models.CharField(max_length=2000)  # Was 300
    content = RichTextField()
    featured_image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    
    categories = models.ManyToManyField(BlogCategory, blank=True)
    tags = models.ManyToManyField(BlogTag, blank=True)
    
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    
    # SEO - INCREASED
    meta_title = models.CharField(max_length=1000, blank=True)  # Was 100
    meta_description = models.CharField(max_length=2000, blank=True)  # Was 200
    
    # Reading time
    reading_time = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:1000]
        if not self.meta_title:
            self.meta_title = self.title[:1000]
        if not self.meta_description:
            self.meta_description = self.excerpt[:2000]
        # Calculate reading time (approx 200 words per minute)
        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 200))
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})
    
    def increment_view_count(self):
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])