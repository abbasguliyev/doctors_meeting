# Generated by Django 4.2 on 2023-04-19 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_appointmentrequest_appointment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentrequest',
            name='doctor_request',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Waiting', 'Waiting'), ('Rejected', 'Rejected')], default='Waiting', max_length=20),
        ),
        migrations.AlterField(
            model_name='appointmentrequest',
            name='request_status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=20),
        ),
    ]
