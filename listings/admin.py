from django.contrib import admin

from .models import Listing

# Register your models here.


class ListingAdmin(admin.ModelAdmin):
    list_display= ('id', 'title', 'is_published', 'price', 'list_date', 'seller','update_date')
    list_display_links= ('id', 'title')
    list_filter= ('seller','list_date','update_date',)
    list_editable=('is_published',)
    search_fields= ('title', 'discription','cpu','ram', 'price' )
    list_per_page=20

admin.site.register(Listing,ListingAdmin)