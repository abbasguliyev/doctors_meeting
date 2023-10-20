# Generated by Django 4.2 on 2023-06-08 09:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0013_ads_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='ads_image',
            field=models.ImageField(blank=True, null=True, upload_to='advertisement', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])]),
        ),
        migrations.CreateModel(
            name='AdsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('ads', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='pages.ads')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
