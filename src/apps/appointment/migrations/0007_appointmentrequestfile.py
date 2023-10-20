# Generated by Django 4.2 on 2023-07-10 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0028_alter_patientsfile_patient'),
        ('appointment', '0006_appointmentrequest_availability'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentRequestFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='appointment.appointmentrequest')),
                ('patient_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_requests', to='authentication.patientsfile')),
            ],
        ),
    ]
