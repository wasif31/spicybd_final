
import math as M
from django.db import models
from carts.models import Cart
from addresses.models import Addresses
from django.db.models.signals import pre_save, post_save
from bingo_project.utils import unique_order_id_generator
from billing.models import BillingProfile
from django.urls import reverse
ORDER_STATUS_CHOICE = (
    ('processing', 'Processing'),
    ('created', 'CREATED'),
    ('paid', 'PAID'),
    ('shipped', 'SHIPPING'),
    ('refunded', 'REFUNDED')
)


class OrderManagerQuerySet(models.query.QuerySet):

    def not_created(self):
        return self.exclude(status='created')

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self.db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset()#..filter(billing_profile=billing_profile,
                                       # cart=cart_obj, active=True, status='created') dile if 1 order place hoy,se ar order dita parbe na
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(
        BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, blank=True)

    # shipping_address
    # billing_profile
    shipping_address = models.ForeignKey(
        Addresses, related_name="shipping_address", on_delete=models.CASCADE, blank=True, null=True)
    billing_address = models.ForeignKey(
        Addresses, related_name="billing_address", on_delete=models.CASCADE, blank=True, null=True)
    billing_profile = models.ForeignKey(
        BillingProfile, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=120, default='created', choices=ORDER_STATUS_CHOICE)
    shipping_total = models.DecimalField(
        default=40.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("orders:details", kwargs={'order_id': self.order_id})

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = M.fsum([shipping_total, cart_total])
        formatted_total = format(new_total, '.2f')
        self.total = new_total
        self.save()
        return new_total

    def __str__(self):
        return self.order_id
# using pre_save singnals with unique_order_generator for saving the unique order id

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        shipping_address = self.shipping_address

        if billing_profile and billing_address and shipping_address and self.total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status

    def __str__(self):
        return self.order_id
    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp', '-updated']


def pre_save_order_id(sender, instance, *args, **kewarg):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    qs = Order.objects.filter(cart=instance.cart).exclude(
        billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_order_id, sender=Order)

# using post save for cart total


def post_save_cart_total(sender, instance, created, *args, **kewarg):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
