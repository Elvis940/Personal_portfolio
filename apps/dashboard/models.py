from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class AdminUser(models.Model):
    """Custom admin user for dashboard access"""
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"
    
    def __str__(self):
        return self.email