# Generated by Django 4.2.4 on 2023-10-23 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0006_alter_motorcycle_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motorcycle',
            name='capacity',
            field=models.IntegerField(),
        ),
    ]
