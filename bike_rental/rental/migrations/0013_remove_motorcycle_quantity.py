# Generated by Django 4.2.7 on 2023-11-27 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0012_alter_motorcycle_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motorcycle',
            name='quantity',
        ),
    ]
