#import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Cart
from django.http import JsonResponse
from orders.models import Order, OrderManager
from listings.models import Listing
from billing.models import BillingProfile
from django.core.exceptions import ObjectDoesNotExist
from account.forms import GuestForm
from django.contrib.auth.decorators import login_required
from account.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Addresses
from billing.models import BillingProfile


# Create your views here.
def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [
        {
            "title": x.title,
            "price": x.price,
            "url": x.get_absolute_url(),
            "id": x.id,
            "slug": x.slug
        } for x in cart_obj.products.all()]

    # products_list = []
    # for x in cart_obj.products.all():
    #     products_list.append({"title:":x.title, "price":x.price})

    cart_data = {"products": products,
                 "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        "cart": cart_obj,
    }

    return render(request, 'carts/home.html', context)


def cart_update(request):
     # getting the product_id which is sent from the update_cart.html
    product_id = request.POST.get('product_id')
    # if the product_id is not none then we taking it to product_obj
    if product_id is not None:
        try:
            product_obj = Listing.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            data_added = False
        else:
            cart_obj.products.add(product_obj)

            data_added = True
        request.session['total_product'] = cart_obj.products.count()
        if request.is_ajax():
            # print("Ajax request")
            json_data = {
                'added': data_added,
                'removed': not data_added,
                'itemCount': cart_obj.products.count(),
            }
            return JsonResponse(json_data)
    # cart_obj.save()
    return redirect("cart:home")
    # return render(request, 'listings/listing.html', {'listing': product_obj})

    # def home(request):
    #     return render(request, 'carts/home.html')


@login_required
def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    guest_form = GuestForm()
    address_form = AddressForm()
    #guest_email_id = request.session.get('guest_email_id')
    # login_form = LoginForm()
    # guest_form = GuestForm()

    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    if not request.user.is_authenticated:
        billing_profile = None

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request)
    has_card = False
    address_qs = None

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Addresses.objects.filter(
                billing_profile=billing_profile)
        order_obj, order_obj_created = Order .objects.new_or_get(
            billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Addresses.objects.get(
                id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

        # has_card = billing_profile.has_card
    if request.method == "POST":
        "check the cart process done"
        is_prepared = order_obj.check_done()
        if is_prepared:
            order_obj.mark_paid()
            request.session['cart_item'] = 0
            del request.session['cart_id']
            return redirect("cart:success")
        else:
            print(crg_msg)
            return redirect("cart:checkout")

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "guest_form": guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
        "has_card": has_card,
        # "publish_key": STRIPE_PUB_KEY
    }
    return render(request, 'carts/checkout.html', context)


def checkout_done(request):
    return render(request, 'carts/checkout-done.html', {})
