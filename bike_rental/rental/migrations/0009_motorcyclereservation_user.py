# Generated by Django 4.2.4 on 2023-11-01 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rental', '0008_alter_motorcycle_fuel_capacity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='motorcyclereservation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
