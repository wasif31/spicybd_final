from django.shortcuts import render
from django.forms import forms
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from listings.models import Listing
from .carts2 import Cart
from .forms import CartAddProductForm, CCartAddProductForm
from django.views.decorators.cache import never_cache


# @require_POST
def cart_add(request, listing_id):
    # create a new cart object passing it the request object
    cart = Cart(request)
    listing = get_object_or_404(Listing, id=listing_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(listing=listing,
                 quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('carts2:cart_detail')


def cart_remove(request, listing_id):
    cart = Cart(request)
    listing = get_object_or_404(Listing, id=listing_id)
    cart.remove(listing)
    return redirect('carts2:cart_detail')


@never_cache
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        maximum_quantity = Listing.objects.get(
            id=item['listing'].id).stock
        PRODUCT_QUANTITY_CHOICES = [(i, str(i))
                                    for i in range(1, maximum_quantity)]

        form = CCartAddProductForm(PRODUCT_QUANTITY_CHOICES,
                                   initial={'quantity': item['quantity'], 'update': True})
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

        item['update_quantity_form'] = form
    return render(request, 'carts/carts_new_details.html', {'cart': cart})
