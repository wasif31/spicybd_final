from django.urls import path
from . import views

urlpatterns = [

    path('signin/', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register/guest', views.guest_register_view, name='guest_register'),
    path('profile/', views.AccountHomeView.as_view(), name='user_profile'),




]
