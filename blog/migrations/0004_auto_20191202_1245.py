# Generated by Django 2.2.3 on 2019-12-02 06:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20191202_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 2, 6, 45, 29, 799949, tzinfo=utc)),
        ),
    ]