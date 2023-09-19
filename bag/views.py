from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from products.models import Product
from bag.templatetags import bag_filters



def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add a quantity of a product to the bag using item_id
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', '/')
    bag = request.session.get('bag', {})

    item_attributes = {}  # You can store item-specific attributes here

    if 'size' in request.POST:
        item_attributes['size'] = request.POST['size']

    if item_id in bag:
        # Existing bag entry
        if 'items_by_quantity' in bag[item_id]:
            bag[item_id]['items_by_quantity'] += quantity
            if item_attributes:
                bag[item_id]['attributes'].update(item_attributes)
        else:
            bag[item_id]['items_by_quantity'] = quantity
            if item_attributes:
                bag[item_id]['attributes'] = item_attributes
    else:
        # New bag entry
        bag[item_id] = {
            'items_by_quantity': quantity,
            'attributes': item_attributes
        }

    messages.success(request, f'Updated {product.name} in your bag.')

    request.session['bag'] = bag
    return redirect(redirect_url)
