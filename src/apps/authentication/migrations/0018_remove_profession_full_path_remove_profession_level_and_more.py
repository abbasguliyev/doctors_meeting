# Generated by Django 4.2 on 2023-04-30 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_doctorprofile_city_doctorprofile_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profession',
            name='full_path',
        ),
        migrations.RemoveField(
            model_name='profession',
            name='level',
        ),
        migrations.RemoveField(
            model_name='profession',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='profession',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='profession',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='profession',
            name='tree_id',
        ),
    ]
