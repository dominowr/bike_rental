# Generated by Django 4.2.7 on 2023-12-08 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_alter_newsimages_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/news'),
        ),
    ]
