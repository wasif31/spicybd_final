"""bingo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from addresses.views import checkout_address_created_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view

urlpatterns = [
    path('', include('pages.urls')),
    path('listings/', include('listings.urls')),
    path('sellers/', include('sellers.urls')),
    path('accounts/', include('account.urls')),
    path('carts/', include('carts.urls')),
    path('blog/', include('blog.urls')),
    path('cart/', include('carts2.urls')),
    path('orders2/', include('orders2.urls')),
    # mapping address view
    path('checkout_address_created_view/',
         checkout_address_created_view, name='checkout_address_created'),
    path('checkout/address/reuse/view/',
         checkout_address_reuse_view, name='checkout_address_reuse'),
    path('api/cart/', cart_detail_api_view, name='api-cart'),

    path('orders/', include("orders.urls", namespace='orders')),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
