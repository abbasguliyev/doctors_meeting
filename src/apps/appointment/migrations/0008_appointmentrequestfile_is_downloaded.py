# Generated by Django 4.2 on 2023-07-13 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0007_appointmentrequestfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentrequestfile',
            name='is_downloaded',
            field=models.BooleanField(default=False),
        ),
    ]
