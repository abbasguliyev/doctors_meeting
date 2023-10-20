# Generated by Django 4.2 on 2023-04-12 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_doctorprofile_id_card_patientsfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorprofile',
            name='id_card',
        ),
        migrations.AddField(
            model_name='user',
            name='id_card',
            field=models.FileField(blank=True, null=True, upload_to='doctors/id_card_upload'),
        ),
    ]