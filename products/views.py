from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Fetch initial queryset and initialize variables
    products = Product.objects.all()
    categories = Category.objects.all()
    query = None
    sort_by = None
    direction = None
    filtered_categories = None

    # Check for GET parameters
    if request.GET:
        # Handle sorting
        if 'sort_by' in request.GET:
            sort_by = request.GET['sort_by']
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
            products = products.order_by(sort_order)

        # Handle category filter
        if 'category' in request.GET:
            filtered_categories = request.GET['category'].split(',')
            products = products.filter(
                category__name__in=filtered_categories
            )
            filtered_categories = Category.objects.filter(
                name__in=filtered_categories
            )

        # Handle search queries
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))          
            queries = Q(
                name__icontains=query
            ) | Q(
                description__icontains=query
            )
            products = products.filter(
                queries
            ).order_by(Lower('name'), Lower('description'))

    # Prepare context for template
    context = {
        'products': products,
        'search_term': query,
        'categories': categories,
        'sort_by': sort_by
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)
