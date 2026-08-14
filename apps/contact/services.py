from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from .models import ContactMessage


class ContactEmailService:
    """Service for sending contact-related emails"""
    
    @staticmethod
    def send_contact_notification(message: ContactMessage):
        """
        Send email notification to admin when a new contact message is received
        """
        try:
            # Admin notification email
            subject = f'New Contact Message: {message.subject}'
            
            # HTML email template
            html_content = render_to_string('contact/emails/admin_notification.html', {
                'message': message,
                'site_name': getattr(settings, 'SITE_NAME', 'Elvis T. Harmon'),
                'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000'),
            })
            
            # Plain text fallback
            text_content = strip_tags(html_content)
            
            # Send to admin
            admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
            
            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                reply_to=[message.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            return True
        except Exception as e:
            print(f"Error sending admin notification: {e}")
            return False
    
    @staticmethod
    def send_auto_reply(message: ContactMessage):
        """
        Send auto-reply to the sender
        """
        try:
            subject = f'Thank you for contacting Elvis T. Harmon'
            
            # HTML email template
            html_content = render_to_string('contact/emails/auto_reply.html', {
                'message': message,
                'site_name': 'Elvis T. Harmon',
                'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000'),
            })
            
            # Plain text fallback
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [message.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            return True
        except Exception as e:
            print(f"Error sending auto-reply: {e}")
            return False
    
    @staticmethod
    def send_status_update(message: ContactMessage, old_status: str):
        """
        Send notification when message status changes
        """
        try:
            status_display = dict(ContactMessage.Status.choices)
            
            subject = f'Your inquiry status has been updated'
            
            html_content = render_to_string('contact/emails/status_update.html', {
                'message': message,
                'old_status': status_display.get(old_status, old_status),
                'new_status': status_display.get(message.status, message.status),
                'site_name': 'Elvis T. Harmon',
                'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000'),
            })
            
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [message.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            return True
        except Exception as e:
            print(f"Error sending status update: {e}")
            return False