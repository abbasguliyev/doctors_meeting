# Generated by Django 4.2 on 2023-05-02 17:43

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_center', '0002_beautycenter_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beautycenter',
            name='about',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
