

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    product_type = models.CharField(max_length=200, default=' ')
    phone_number = models.CharField(max_length=100)
    product_logo = models.ImageField(upload_to='profile_images/%Y/%m/%d/',
                                     max_length=255, blank=True, default='profile_images/default/default.jpg')
    created_at = models.DateTimeField(default=timezone.now())
    description = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return '"%s %s"' % (self.product_type, self.product_name)

    def save(self):
        if not self.id:
            self.created_at = timezone.now()
        self.last_updated = timezone.now()
        super(Album, self).save()

    def was_published_recently(self):
        if self.created_at >= timezone.now() - datetime.timedelta(seconds=20):
            return 'Just now'
        elif self.created_at >= timezone.now() - datetime.timedelta(minutes=1):
            return str((timezone.now() - self.created_at).seconds) + ' seconds ago'
        elif self.created_at >= timezone.now() - datetime.timedelta(minutes=60):
            return str(int((timezone.now() - self.created_at).seconds/60)) + ' minutes ago'
        elif self.created_at >= timezone.now() - datetime.timedelta(hours=24):
            return str(int((timezone.now() - self.created_at).seconds/3600)) + ' hours ago'
        elif self.created_at >= timezone.now() - datetime.timedelta(days=365):
            return str((timezone.now() - self.created_at).days) + ' days ago'
        else:
            return 'Created at: ' + str(self.created_at.year)+'-'+str(self.created_at.month)+'-'+str(self.created_at.day)+' ' + str(self.created_at.hour) + ':'+str(self.created_at.minute) + ':' + str(self.created_at.second)
