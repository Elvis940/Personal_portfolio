from django import forms
from django.core.validators import MinLengthValidator
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form for the portfolio"""
    
    class Meta:
        model = ContactMessage
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'subject', 'project_type', 'budget', 'timeline', 'message'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief subject',
                'required': True
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'budget': forms.Select(attrs={
                'class': 'form-select'
            }),
            'timeline': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell me about your project...',
                'required': True
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number (optional)',
            'subject': 'Subject',
            'project_type': 'Project Type',
            'budget': 'Budget Range',
            'timeline': 'Timeline',
            'message': 'Your Message',
        }
    
    def clean_message(self):
        """Validate message length"""
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        if len(message) > 5000:
            raise forms.ValidationError('Message is too long. Please limit to 5000 characters.')
        return message