# Generated by Django 4.2.7 on 2024-01-11 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0014_motorcyclereservation_is_deleted'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='motorcyclereservation',
            unique_together={('start_date', 'end_date', 'is_deleted')},
        ),
    ]
