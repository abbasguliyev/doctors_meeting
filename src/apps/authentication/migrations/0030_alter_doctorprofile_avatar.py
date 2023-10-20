# Generated by Django 4.2 on 2023-08-14 06:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0029_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='default-photo.png', upload_to='doctors/avatar_upload', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png'])]),
        ),
    ]