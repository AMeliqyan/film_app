# Generated by Django 4.2.3 on 2023-09-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0009_alter_feedback_date_alter_feedback_star_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]