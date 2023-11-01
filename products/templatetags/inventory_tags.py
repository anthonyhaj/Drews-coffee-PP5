from django import template
from products.models import Product

register = template.Library()


@register.filter
def inventory_status(quantity):
    if quantity > 0:
        if quantity <= 3:
            return f'Only {quantity} left in stock - Hurry!'
        else:
            return f'In stock ({quantity} available)'
    else:
        return 'Out of Stock!'
