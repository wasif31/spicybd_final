from django.conf.urls import url
from . import views
from django.urls import path
app_name = 'orders2'

urlpatterns = [
    path('create/', views.order_create, name='order_create')
]
