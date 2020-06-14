from django.db import models
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Seller(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    is_mvp = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    category_name = models.CharField(max_length=150, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True, on_delete=models.CASCADE)
    slug = models.SlugField()
    category_created_at = models.DateTimeField(
        default=datetime.now, blank=True)
    category_updated_at = models.DateTimeField(
        default=datetime.now, blank=True)

    photo_category = models.ImageField(
        default=True, upload_to='photos/%Y/%m/%d/')

    class MPTTMeta:
        order_insertion_by = ['category_name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = "categories"

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    def __str__(self):
        return self.category_name


def slider_upload(unstance, filename):
    return 'photos/slider/%Y/%m/%d/' % (filename)


class Slider(models.Model):

    image = models.ImageField(upload_to='photos/slider/%Y/%m/%d/')
    order = models.IntegerField(default=0)
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True, blank=True)

    class Meta:
        ordering = ['order', '-start_date', '-end_date']

    def __str__(self):
        return str(self.image)
