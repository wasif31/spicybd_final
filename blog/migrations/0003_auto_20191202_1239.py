# Generated by Django 2.2.3 on 2019-12-02 06:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20191115_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 2, 6, 39, 19, 205875, tzinfo=utc)),
        ),
    ]