from django.db import models
from django.urls import reverse
from datetime import datetime
from sellers.models import Seller, Category
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Listing(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    # adress
    brand = models.CharField(max_length=200)
    category = TreeForeignKey(
        Category, null=True, blank=True, on_delete=models.DO_NOTHING)
    # city=models.CharField(max_length=200)
    # state=models.CharField(max_length=200)
    # zipcode=models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # blank=true means not mandatory to add the info
    price = models.IntegerField()
    # small_des_1  bed
    details1 = models.CharField(max_length=200)
    # small_des_2  bath models.DecimalField (max_digits=2,decimal_places =1 ) omnly one decimal available like 1.5
    details2 = models.CharField(max_length=200)
    # small_des_3  garra (default=0)
    details3 = models.CharField(max_length=200, blank=True)
    # small_des_4  sqft
    details4 = models.CharField(max_length=200, blank=True)
    # lot size max digit=2 means 2 er beshi hote parbe na

    other1 = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)

    #  photo

    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    stock = models.PositiveIntegerField()
    #list_date=models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

    def get_cat_list(self):
        k = self.category  # for now ignore this instance method

        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    # def get_absolute_url(self):
    #     #         # first way
    #     #         # return f"/products/{self.slug}/"

    #     #         # most effictive way
    #     return reverse('listing', kwargs={'pk': self.pk})
    def get_absolute_url(self):
        return reverse('listing', args=[self.id])
