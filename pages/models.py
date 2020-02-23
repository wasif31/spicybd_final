from django.db import models

# Create your models here.
from django.db import models


class Varify_Order(models.Model):
    order_id = models.CharField(max_length=300)
    transaction_id = models.CharField(max_length=300)
    bkash_number = models.IntegerField()
