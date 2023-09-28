from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def blog_list(request):
    blogs = BlogPost.objects.filter(status=1).order_by('-created_date')
    return render(request, 'blog/blog.html', {'blogs': blogs})


def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/blog_detail.html', {'blog': blog})