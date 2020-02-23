# Generated by Django 2.2.3 on 2019-12-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='cpu',
            new_name='details1',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='graphics',
            new_name='details2',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='ram',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='rom',
        ),
        migrations.AddField(
            model_name='listing',
            name='details3',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='listing',
            name='details4',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='listing',
            name='stock',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]