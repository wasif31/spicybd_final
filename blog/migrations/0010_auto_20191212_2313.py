# Generated by Django 2.2.3 on 2019-12-12 17:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20191210_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 17, 13, 0, 408681, tzinfo=utc)),
        ),
    ]
