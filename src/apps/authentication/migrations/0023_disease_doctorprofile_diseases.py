# Generated by Django 4.2 on 2023-05-30 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0022_doctorprofile_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='diseases',
            field=models.ManyToManyField(to='authentication.disease'),
        ),
    ]
