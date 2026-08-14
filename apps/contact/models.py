from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone


class ContactMessage(models.Model):
    """Model for storing contact form submissions"""
    
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        CONTACTED = 'CONTACTED', 'Contacted'
        IN_DISCUSSION = 'IN_DISCUSSION', 'In Discussion'
        COMPLETED = 'COMPLETED', 'Completed'
        ARCHIVED = 'ARCHIVED', 'Archived'
    
    class ProjectType(models.TextChoices):
        WEB_DEVELOPMENT = 'WEB_DEVELOPMENT', 'Web Development'
        DJANGO_DEVELOPMENT = 'DJANGO_DEVELOPMENT', 'Django Development'
        AI_ML = 'AI_ML', 'AI/ML Development'
        API_DEVELOPMENT = 'API_DEVELOPMENT', 'API Development'
        DATABASE_DEVELOPMENT = 'DATABASE_DEVELOPMENT', 'Database Development'
        SOFTWARE_ENGINEERING = 'SOFTWARE_ENGINEERING', 'Software Engineering'
        TECHNICAL_CONSULTING = 'TECHNICAL_CONSULTING', 'Technical Consulting'
        OTHER = 'OTHER', 'Other'
    
    class BudgetRange(models.TextChoices):
        UNDER_1000 = 'UNDER_1000', 'Under $1,000'
        _1000_5000 = '_1000_5000', '$1,000 - $5,000'
        _5000_10000 = '_5000_10000', '$5,000 - $10,000'
        _10000_25000 = '_10000_25000', '$10,000 - $25,000'
        _25000_50000 = '_25000_50000', '$25,000 - $50,000'
        _50000_PLUS = '_50000_PLUS', '$50,000+'
        NOT_SPECIFIED = 'NOT_SPECIFIED', 'Not Specified'
    
    class Timeline(models.TextChoices):
        URGENT = 'URGENT', 'Urgent (Within 1 week)'
        SHORT = 'SHORT', 'Short (1-4 weeks)'
        MEDIUM = 'MEDIUM', 'Medium (1-3 months)'
        LONG = 'LONG', 'Long (3-6 months)'
        FLEXIBLE = 'FLEXIBLE', 'Flexible'
        NOT_SPECIFIED = 'NOT_SPECIFIED', 'Not Specified'
    
    # Contact Information - INCREASED FIELD LENGTHS
    first_name = models.CharField(max_length=100)  # Was 50
    last_name = models.CharField(max_length=100)   # Was 50
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Message Details - INCREASED FIELD LENGTHS
    subject = models.CharField(max_length=300)  # Was 200
    project_type = models.CharField(
        max_length=50,  # Was 30 - THIS WAS THE MAIN ISSUE
        choices=ProjectType.choices,
        default=ProjectType.OTHER
    )
    budget = models.CharField(
        max_length=30,  # Was 20
        choices=BudgetRange.choices,
        default=BudgetRange.NOT_SPECIFIED
    )
    timeline = models.CharField(
        max_length=30,  # Was 20
        choices=Timeline.choices,
        default=Timeline.FLEXIBLE
    )
    message = models.TextField(validators=[MinLengthValidator(10)])
    
    # Status Tracking - INCREASED FIELD LENGTHS
    status = models.CharField(
        max_length=30,  # Was 20
        choices=Status.choices,
        default=Status.NEW
    )
    notes = models.TextField(blank=True, help_text="Internal notes for admin")
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contacted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject[:30]}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def mark_contacted(self):
        """Mark the message as contacted"""
        self.status = self.Status.CONTACTED
        self.contacted_at = timezone.now()
        self.save()
    
    def update_status(self, new_status):
        """Update the status of the message"""
        if new_status in [choice[0] for choice in self.Status.choices]:
            self.status = new_status
            if new_status == self.Status.CONTACTED and not self.contacted_at:
                self.contacted_at = timezone.now()
            self.save()
            return True
        return False