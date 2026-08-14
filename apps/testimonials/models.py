from django.db import models
from django.core.validators import FileExtensionValidator


class Testimonial(models.Model):
    """Client testimonials"""
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(
        default=5, 
        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]
    )
    image = models.ImageField(
        upload_to='testimonials/',
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
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.company}"
    
    @property
    def full_name(self):
        return f"{self.name} {self.position}"
    
    def get_rating_stars(self):
        """Return HTML for star rating"""
        stars = ''
        for i in range(5):
            if i < self.rating:
                stars += '<i class="fas fa-star text-warning"></i>'
            else:
                stars += '<i class="far fa-star text-muted"></i>'
        return stars