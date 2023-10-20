# Generated by Django 4.2 on 2023-06-08 10:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_alter_ads_ads_image_adscomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='adscomment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adscomment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
