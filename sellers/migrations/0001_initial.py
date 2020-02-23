# Generated by Django 2.2.3 on 2019-11-15 08:01

import datetime
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('description', models.TextField(blank=True)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('is_mvp', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField()),
                ('category_created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('category_updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('photo_category', models.ImageField(default=True, upload_to='photos/%Y/%m/%d/')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='sellers.Category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'unique_together': {('parent', 'slug')},
            },
        ),
    ]