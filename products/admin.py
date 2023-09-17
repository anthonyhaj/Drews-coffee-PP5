from django.contrib import admin
from .models import Category, Product

from django.contrib import admin
from .models import Product, Category, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', )
    ordering = ('product',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'category', 'rating')
    ordering = ('name',)
    search_fields = ('name', 'sku', 'category__name')
    list_filter = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    ordering = ('name',)
    search_fields = ('name', 'friendly_name')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
