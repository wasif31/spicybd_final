from django.shortcuts import render
from .models import Listing
from django.shortcuts import get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, brand_choices, category_choices, sort_choices
from django.views import generic
from carts.models import Cart
from django.shortcuts import render, get_object_or_404, Http404
from sellers.models import *
from sellers.views import *
from carts2.forms import CartAddProductForm

# Create your views here.


def index(request):
    listings = Listing.objects.all().filter(is_published=True)
    paginator = Paginator(listings, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    # pk=primary key meant
    cart_product_form = CartAddProductForm()
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(title__icontains=keywords)

    # brands
    if 'brand' in request.GET:
        brand = request.GET['brand']
        if brand:
            queryset_list = queryset_list.filter(brand__iexact=brand)
   # category
    if 'category' in request.GET:
        category = request.GET['category']
        # print(category)

        if category:
            queryset_list = queryset_list.filter(
                category__category_name__iexact=category)
   # sortby will work later
   # iexact or sort_by_lte ...lte means less than or equal
   #
   # price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
   # sortby will work later
    if 'sort_by' in request.GET:
        sort_by = request.GET['sort_by']
        # print(sort_by)
        if sort_by == 'PRICE_LOW_TO_HIGH':
            # print(sort_by)
            queryset_list = queryset_list.order_by('price')
        if sort_by == 'PRICE_HIGH_TO_LOW':
            # print(sort_by)
            queryset_list = queryset_list.order_by('price').reverse()
        if sort_by == 'NEWEST_ADDED':
            queryset_list = queryset_list.order_by('list_date').reverse()
    context = {
        'category_choices': category_choices,
        'price_choices': price_choices,
        'brand_choices': brand_choices,
        'sort_choices': sort_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)


class ProductIdDetailView(generic.DetailView):
    cart_product_form = CartAddProductForm()
    queryset = Listing.objects.all()
    template_name = "listings/listing.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductIdDetailView,
                        self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        #request = self.request
        pk = self.kwargs['pk']
        try:
            instance = Listing.objects.get(pk=pk)
        except Listing.DoesNotExist:
            raise Http404("Product not exist")
        except Listing.MultipleObjectsReturned:
            qs = Listing.objects.filter(pk=pk)
            instance = qs.first()
        except:
            raise Http404("don't bother..")

        return instance


def product_detail(request, id, slug):
    listing = get_object_or_404(Listing, id=id, available=True)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)
