from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    STATUS_CHOICES = (
        (0, 'Draft'),
        (1, 'Published'),
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    tags = models.CharField(max_length=100, blank=True, null=True)  # New field

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title
