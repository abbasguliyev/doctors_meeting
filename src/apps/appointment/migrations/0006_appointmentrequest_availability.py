# Generated by Django 4.2 on 2023-04-19 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0005_alter_appointmentrequest_doctor_request_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentrequest',
            name='availability',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_request', to='appointment.availability'),
            preserve_default=False,
        ),
    ]
