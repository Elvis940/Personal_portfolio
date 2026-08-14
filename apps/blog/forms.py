from django import forms
from apps.blog.models import BlogPost, BlogCategory, BlogTag
from ckeditor.widgets import CKEditorWidget


class BlogPostForm(forms.ModelForm):
    """Form for creating and editing blog posts"""
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'excerpt', 'content', 'featured_image',
            'categories', 'tags', 'is_featured', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary of the post'}),
            'content': CKEditorWidget(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set empty label for categories and tags
        self.fields['categories'].required = False
        self.fields['tags'].required = False
        self.fields['featured_image'].required = False