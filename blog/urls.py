from django.urls import include, path
from .models import Album
from .import views
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
app_name = 'music'

urlpatterns = [
    
    path('', views.IndexView.as_view(), name='index2'),
    path('<int:pk>/', views.DetailView.as_view(), name='details'),

    
    path('album/create_album/',
         views.AlbumCreateView.as_view(), name='create_album'),
    
    #     This approach applies the decorator on a per-instance basis. If you want every instance of a view to be decorated, you need to take a different approach.
    path('album/<int:pk>/update/',
         login_required(views.AlbumUpdateView.as_view()), name='album-update'),
]
