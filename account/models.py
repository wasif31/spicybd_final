from django.db import models

# Create your models here.


class GuestEmail(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    # full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)     # can login
    # staff   = models.BooleanField(default=False)    # staff user non super user
    # admin   = models.BooleanField(default=False)    # superuser
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # __unicode__ return
        return self.email
