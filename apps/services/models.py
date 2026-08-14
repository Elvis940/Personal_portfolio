from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator


class Service(models.Model):
    """Services offered"""
    
    name = models.CharField(max_length=500)  # Was 100
    slug = models.SlugField(max_length=1000, unique=True, blank=True)  # Was default
    description = models.TextField()
    features = models.TextField(blank=True, help_text="List of features, one per line")
    technologies = models.TextField(blank=True, help_text="Technologies used, comma separated")
    icon = models.CharField(max_length=200, blank=True, help_text="FontAwesome icon class")  # Was 50
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:1000]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_features_list(self):
        """Return features as a list"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []
    
    def get_technologies_list(self):
        """Return technologies as a list"""
        if self.technologies:
            return [t.strip() for t in self.technologies.split(',') if t.strip()]
        return []