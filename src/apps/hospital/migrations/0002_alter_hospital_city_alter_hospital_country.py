# Generated by Django 4.2 on 2023-04-30 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]