from django.contrib import admin

from .models import Seller, Category,Slider
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin


class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'date_added',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20


admin.site.register(Seller, SellerAdmin)


class CategoryAdmin(admin.ModelAdmin):
    category_display = ('category_name', 'category_slug',
                        'category_created_at', 'category_updated_at', 'photo_category')


admin.site.register(Category, DraggableMPTTAdmin)


class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'order', 'start_date',
                    'end_date', 'active', 'featured')
    list_editable = ['order']

    class Meta:
        model = Slider


admin.site.register(Slider, SliderAdmin)
