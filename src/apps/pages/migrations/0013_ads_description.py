# Generated by Django 4.2 on 2023-06-07 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_ads_delete_advertisementmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='description',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
    ]