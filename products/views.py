# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd Party
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Internal
from .models import Product, Category
from .forms import ProductForm
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
                messages.error(request, "You didn't enter any \
                     search criteria!")
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
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product \
                to the shop!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure \
                the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    Delete product from the shop
    """
    if not request.user.is_superuser:
        messages.error(request, 'Only Admins owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product has been deleted.')

    return redirect(reverse('products'))


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product \
                in the shop!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure \
                the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)
