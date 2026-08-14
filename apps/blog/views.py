from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import BlogPost, BlogCategory, BlogTag


def blog_list(request):
    """Blog listing page"""
    posts = BlogPost.objects.filter(is_published=True).prefetch_related('categories', 'tags')
    
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(categories__slug=category_slug)
    
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    featured_post = posts.filter(is_featured=True).first()
    posts = posts.order_by('-created_at')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = BlogCategory.objects.annotate(post_count=Count('blogpost'))
    tags = BlogTag.objects.annotate(post_count=Count('blogpost'))
    
    context = {
        'posts': page_obj,
        'featured_post': featured_post,
        'categories': categories,
        'tags': tags,
        'search_query': search_query,
        'current_category': category_slug,
        'current_tag': tag_slug,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """Blog post detail page"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    post.view_count = post.view_count + 1
    post.save(update_fields=['view_count'])
    
    # Get related posts (same category)
    related_posts = BlogPost.objects.filter(
        categories__in=post.categories.all(),
        is_published=True
    ).exclude(id=post.id).distinct()[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    
    return render(request, 'blog/blog_detail.html', context)