# Generated by Django 2.2.3 on 2019-12-02 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=100),
        ),
    ]
