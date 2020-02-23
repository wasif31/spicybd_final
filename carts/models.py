from django.conf import settings
import math
from django.db import models
from listings.models import Listing
from django.db.models.signals import pre_save, post_save, m2m_changed
User = settings.AUTH_USER_MODEL
# Create your models here.


class CartManager(models.Manager):
    def new_or_get(self, request):
         # del request.session['cart_id']
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()

        else:
            cart_obj = Cart.objects.new_cart(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    # print(request.session)
    # request.season.set_expiry(300) 5min auto expire
    # request.season.season_key
    # 'season_key','set_expiry'

    def new_cart(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(Listing, blank=True)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CartManager()

    def __str__(self):
        return str(self.id)


"""
using m2m signal we are managing calcultion of cart.
"""

# creating signal so that we can calculate our products at the time of shopping


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        
        for x in products:
            total += x.price
            print(total)
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


# calculating subtotal like delevary cost etc .....
def pre_save_cart_receiver(sender, instance, *args, **kwargs):

    instance.total = math.fsum([instance.subtotal, 2])  # *1.08
    # instance.total=float(instance.subtotal)*float(1.08)


pre_save.connect(pre_save_cart_receiver, sender=Cart)
