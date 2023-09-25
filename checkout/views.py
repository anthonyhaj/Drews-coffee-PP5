from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key':
            'pk_test_51NuAtwE8SqEUAzxcugJBYioARoAALWC7qE68tnfnoPGChxOCl5iHXcHe1KGwjvqgC1l4Ospzb6FBZnILtsr8cL2m003wE3rELY',
            'client_secret': 'test client secret',
    }

    return render(request, template, context)