from django.urls import path
from . import views
#app_name = 'listings'
# app_name = 'listings'
urlpatterns = [

    path('', views.index, name='listings'),
    # path('<int:pk>/', views.ProductIdDetailView.as_view(), name='listing'),
    path('<int:listing_id>/', views.listing, name='listing'),
    path('search', views.search, name='search'),
    # path('products/<slug>/', ProductSlugDetailView.as_view(), name='detail'),



]
