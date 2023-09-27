# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd Party
from django.shortcuts import (render, redirect, reverse,
                              HttpResponse, get_object_or_404)
from django.contrib import messages
# Internal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from products.models import Product, Category
from bag.templatetags import bag_filters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def view_bag(request):
    """
     A view that renders the bag contents page
    """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', '/')
    bag = request.session.get('bag', {})
    size = None

    if 'size' in request.POST:
        size = request.POST['size']

    # Check if the item is already in the bag
    if item_id in bag.keys():
        # If it's an int, it's not whats expected. Reset to a dictionary.
        if isinstance(bag[item_id], int):
            bag[item_id] = {}

        if size:
            if 'items_by_size' not in bag[item_id]:
                bag[item_id]['items_by_size'] = {}
            if size in bag[item_id]['items_by_size']:
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            if 'items_by_quantity' not in bag[item_id]:
                bag[item_id]['items_by_quantity'] = 0

            bag[item_id]['items_by_quantity'] += quantity
    else:
        if size:
            bag[item_id] = {'items_by_size': {size: quantity}}
        else:
            bag[item_id] = {'items_by_quantity': quantity}

    messages.success(request, f'Added {product.name} in your bag.')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'size' in request.POST:
        size = request.POST['size']
    bag = request.session.get('bag', {})

    if item_id in bag.keys():
        # If the item exists, but is not a dictionary, reset it.
        if isinstance(bag[item_id], int):
            bag[item_id] = {}

        # Handle the size logic
        if size:
            if 'items_by_size' not in bag[item_id]:
                messages.error(request, f'Size {size.upper()} {product.name} \
                    does not exist in your bag')
                return redirect(reverse('view_bag'))

            if quantity > 0:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(
                    request, f'Updated size {size.upper()} {product.name} \
                        quantity to {bag[item_id]["items_by_size"][size]}'
                )
            else:
                del bag[item_id]['items_by_size'][size]
                if not bag[item_id]['items_by_size']:
                    bag.pop(item_id)
                messages.success(
                    request, f'Removed size {size.upper()} {product.name} \
                        from your bag'
                )
        else:
            if 'items_by_quantity' not in bag[item_id]:
                messages.error(request, f'{product.name} does not exist in \
                     your bag')
                return redirect(reverse('view_bag'))

            if quantity > 0:
                bag[item_id]['items_by_quantity'] = quantity
                messages.success(
                    request, f'Updated {product.name} quantity to \
                         {bag[item_id]["items_by_quantity"]}'
                )
            else:
                bag.pop(item_id)
                messages.success(request, f'Removed {product.name} from \
                     your bag')
    else:
        messages.error(request, f'{product.name} does not exist in your bag')
        return redirect(reverse('view_bag'))

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove the item from the shopping bag
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'size' in request.POST:
            size = request.POST['size']
        bag = request.session.get('bag', {})

        if item_id not in bag.keys():
            messages.error(
                request, f'{product.name} does not exist in your bag'
            )
            return HttpResponse(status=404)

        # If the item exists, but is not a dictionary, simply remove
        if isinstance(bag[item_id], int):
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')
            request.session['bag'] = bag
            return HttpResponse(status=200)

        # Handle the size logic
        if size:
            if 'items_by_size' not in bag[item_id]:
                messages.error(
                    request, f'Size {size.upper()} {product.name} does \
                         not exist in your bag'
                )
                return HttpResponse(status=404)

            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(
                request, f'Removed size {size.upper()} {product.name} from \
                     your bag'
            )
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
