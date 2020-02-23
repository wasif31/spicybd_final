from django.conf.urls import url
from . import views
from django.urls import path
app_name = 'carts2'

urlpatterns = [
    path('add/<int:listing_id>/', views.cart_add, name='cart_add'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<int:listing_id>/', views.cart_remove, name='cart_remove'),
]
