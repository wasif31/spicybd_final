# Generated by Django 2.2.3 on 2019-12-12 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='varify_order',
            name='order_id',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='varify_order',
            name='transaction_id',
            field=models.CharField(max_length=300),
        ),
    ]
