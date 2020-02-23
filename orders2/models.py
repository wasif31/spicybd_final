

# Create your models here.
from django.db import models
from listings.models import Listing

ORDER_STATUS_CHOICE = (
    ('processing', 'Processing'),
    ('created', 'CREATED'),
    ('paid', 'PAID'),
    ('shipped', 'SHIPPING'),
    ('refunded', 'REFUNDED')
)

# class OrderManagerQuerySet(models.query.QuerySet):

#     def not_created(self):
#         return self.exclude(status='created')

#     def by_request(self, request):
#         return self

# class OrderManager(models.Manager):
#     def get_queryset(self):
#         return OrderManagerQuerySet(self.model, using=self.db)

#     def by_request(self, request):
#         return self.get_queryset().by_request(request)

#     def new_or_get(self):
#         created = False
#         qs = self.get_queryset()#..filter(billing_profile=billing_profile,
#                                        # cart=cart_obj, active=True, status='created') dile if 1 order place hoy,se ar order dita parbe na
#         if qs.count() == 1:
#             obj = qs.first()
#         else:
#            pass
#         return obj, created


class Order(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=120, default='created', choices=ORDER_STATUS_CHOICE)
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    # objects = OrderManager()

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    listing = models.ForeignKey(
        Listing, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
