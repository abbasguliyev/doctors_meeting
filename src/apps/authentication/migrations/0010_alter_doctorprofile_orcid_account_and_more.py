# Generated by Django 4.2 on 2023-04-15 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_education_is_continue_experience_is_continue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='orcid_account',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='pubmed_account',
            field=models.URLField(blank=True, null=True),
        ),
    ]
