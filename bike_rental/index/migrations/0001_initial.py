# Generated by Django 4.2.7 on 2023-11-29 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('summary', models.TextField(max_length=250)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField()),
                ('slug', models.SlugField(blank=False)),
            ],
        ),
        migrations.CreateModel(
            name='NewsImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/news')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.news')),
            ],
        ),
    ]
