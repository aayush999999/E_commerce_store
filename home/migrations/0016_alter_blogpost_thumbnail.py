# Generated by Django 4.2.6 on 2023-12-23 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_blogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='thumbnail',
            field=models.ImageField(default='', upload_to='blog/images'),
        ),
    ]
