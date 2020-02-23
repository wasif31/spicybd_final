from .models import Varify_Order
from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Listing
from sellers.models import Seller
from listings.choices import price_choices, brand_choices, category_choices, sort_choices
# Create your views here.
# def index(request):
#  return HttpResponse('<h1>Testing</h1>')


def index(request):
    listings = Listing.objects.order_by(
        '-list_date').filter(is_published=True)[:3]
    context = {
        'listings': listings,
        'category_choices': category_choices,
        'price_choices': price_choices,
        'brand_choices': brand_choices,
        'sort_choices': sort_choices,

    }
    return render(request, 'pages/index.html', context)


def about(request):
    # get all seller
    sellers = Seller.objects.order_by('-date_added')
    # get MvP
    mvp_sellers = Seller.objects.all().filter(is_mvp=True)

    context = {
        'sellers': sellers,
        'mvp_sellers': mvp_sellers
    }
    return render(request, 'pages/about.html', context)


def page_not_found(request):
    return render(request, 'pages/404.html', {})


def vaify_order(request):
    if request.method == 'POST':
        post = Varify_Order()
        post.order_id = request.POST.get('order_id')
        post.transaction_id = request.POST.get('transaction_id')
        post.bkash_number = request.POST.get('bkash_number')

        post.save()

        return render(request, 'orders/varify_order.html')

    else:
        return render(request, 'orders/varify_order.html')
