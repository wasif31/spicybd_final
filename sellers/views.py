from django.shortcuts import render, get_object_or_404
from .models import Category
from listings.models import Listing
# Create your views here.


def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    new_category_slug_list = category_slug[1:]
    new_category_slug = "/".join(new_category_slug_list)
    # print("copy " , new_category_slug)
    
    

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)
        # print("parent",parent)
    if not parent:
        new_category_slug = hierarchy
        # print("root-check",new_category_slug)

    try:
        instance = Category.objects.get(parent=parent, slug=category_slug[-1])
    except:
        instance = get_object_or_404(Listing, slug=category_slug[-1])
        return render(request, "listings/listings.html", {'instance': instance})
    else:
        return render(request, 'pages/categories.html', {'instance': instance, 'hierarchy': new_category_slug})
