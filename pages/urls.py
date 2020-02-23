from django.urls import path
from . import views
urlpatterns = [

    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('page_not_found', views.page_not_found, name='page_not_found'),
    path('varify_order', views.vaify_order, name='varify_order'),



]
