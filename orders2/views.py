from django.shortcuts import render
# Create your views here.
from .models import OrderItem
from .forms import OrderCreateForm
from carts2.carts2 import Cart
from django.views.decorators.cache import never_cache
from listings.models import Listing


def order_create(request):

    cart = Cart(request)
    a = cart.get_total_price()
    print("total cost", cart.get_total_price())
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, initial={
                               'total_cost': cart.get_total_price()})
        print(cart.get_total_price())
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    listing=item['listing'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                previous_listing = Listing.objects.get(
                    id=item['listing'].id)
                print("stock ", previous_listing.stock)
                previous_listing.stock = (
                    previous_listing.stock - item['quantity'])
                previous_listing.save()
            cart.clear()
            form = OrderCreateForm()
        return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm(initial={'total_cost': cart.get_total_price()})
    return render(request, 'orders/create.html', {'form': form})
