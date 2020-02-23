from django.urls import path
from . import views
urlpatterns=[

path('category/<path:hierarchy>', views.show_category,name='category'),
]