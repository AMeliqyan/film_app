# Generated by Django 4.2.3 on 2023-08-23 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='languages',
            field=models.ManyToManyField(to='film.language'),
        ),
    ]
