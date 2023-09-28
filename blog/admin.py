from django.contrib import admin
from .models import BlogPost


# Registration of the post items for the admin panel
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    # Add 'featured_image' to list_display
    list_display = ('title', 'slug', 'status',
                    'created_date', 'updated_date',
                    'author', 'featured_image')

    list_filter = ('status', 'created_date', 'updated_date', 'author')

    search_fields = ['title', 'content', 'tags']

    ordering = ['-created_date']
