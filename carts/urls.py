from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [


    path('', views.cart_home, name='home'),
    path('checkout/', views.checkout_home, name='checkout'),
    path('update/', views.cart_update, name='update'),
    path('checkout/success/', views.checkout_done, name='success'),


]
