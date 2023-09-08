# Generated by Django 4.2.3 on 2023-08-28 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0002_film_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='img',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='film',
            name='video',
            field=models.FileField(default='', upload_to='videos/'),
        ),
    ]
