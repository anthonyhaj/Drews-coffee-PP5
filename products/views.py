from django.shortcuts import render
from .models import Product
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
        )

    # Sorting
    sort_by = request.GET.get('sort_by', 'name')
    
    if sort_by == 'price_low':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_high':
        queryset = queryset.order_by('-price')
    elif sort_by == 'rating_low':
        queryset = queryset.order_by('rating')
    elif sort_by == 'rating_high':
        queryset = queryset.order_by('-rating')
    elif sort_by == 'category_az':
        queryset = queryset.order_by(Lower('category__name'))
    elif sort_by == 'category_za':
        queryset = queryset.order_by(Lower('category__name').desc())
    elif sort_by == 'name_az':
        queryset = queryset.order_by(Lower('name'))
    elif sort_by == 'name_za':
        queryset = queryset.order_by(Lower('name').desc())
    else:
        queryset = queryset.order_by(Lower('name'))

    context = {'products': queryset}
    return render(request, 'products/products.html', context)
