# Generated by Django 4.0.4 on 2022-04-21 00:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_profitperkospi_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profit',
        ),
    ]
