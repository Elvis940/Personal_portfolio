from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, BlogCategory, BlogTag


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'is_featured', 'view_count', 'reading_time', 'created_at']
    list_filter = ['is_published', 'is_featured', 'categories', 'tags']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ['title']}
    readonly_fields = ['view_count', 'reading_time', 'created_at', 'updated_at', 'published_at']
    filter_horizontal = ['categories', 'tags']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Organization', {
            'fields': ('categories', 'tags', 'is_featured', 'is_published')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Statistics', {
            'fields': ('view_count', 'reading_time', 'published_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']