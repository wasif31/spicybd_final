from django.http import HttpResponseRedirect
from django.middleware import http
from django.shortcuts import render
from .models import Album
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/details.html'

    # To decorate every instance of a class-based view, you need to decorate the class definition itself. To do this you apply the decorator to the dispatch() method of the class
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@never_cache
@login_required
# decorators = [never_cache, login_required]
# @method_decorator(decorators, name='dispatch') was changed by the above decorators
def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    return render(request, 'music/details.html', {'album': album})


decorators = [never_cache, login_required]


# the line above is similar to the next commented lines
# @method_decorator(never_cache, name='dispatch')
# @method_decorator(login_required, name='dispatch')
@method_decorator(decorators, name='dispatch')
class AlbumCreateView(CreateView):
    model = Album
    template_name = 'music/album_form.html'
    fields = ['product_name', 'product_type',
              'phone_number', 'product_logo', 'description']

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(AlbumCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('music:index2')


decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
class AlbumUpdateView(UpdateView):
    model = Album
    template_name = 'music/album_update_form.html'
    fields = ['product_name', 'product_type',
              'phone_number', 'product_logo', 'description']

    def get_success_url(self):
        return reverse('music:index2')
