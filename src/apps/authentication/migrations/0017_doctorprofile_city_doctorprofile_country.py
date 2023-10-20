# Generated by Django 4.2 on 2023-04-24 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('authentication', '0016_remove_doctorprofile_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='cities_light.city'),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='cities_light.country'),
        ),
    ]
