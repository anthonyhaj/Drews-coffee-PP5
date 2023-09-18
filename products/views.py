from django.shortcuts import render
from .models import Product, Category
from django.db.models import Q
from django.db.models.functions import Lower


def all_products(request):
    queryset = Product.objects.all()
    query = request.GET.get('q')

    # Search Query
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
            
        ).order_by(Lower('name'), Lower('description'))

    # Sorting
    sort_by = request.GET.get('sort_by', 'name_az')
    sort_options = {
        'price_low': 'price',
        'price_high': '-price',
        'rating_low': 'rating',
        'rating_high': '-rating',
        'category_az': Lower('category__name'),
        'category_za': Lower('category__name').desc(),
        'name_az': Lower('name'),
        'name_za': Lower('name').desc()
    }
    sort_order = sort_options.get(sort_by, Lower('name'))
    queryset = queryset.order_by(sort_order)
    categories = Category.objects.all()
    context = {
        'products': queryset,
        'sort_by': sort_by,
        'categories': categories
    }
    return render(request, 'products/products.html', context)
