# Generated by Django 4.0.4 on 2022-04-20 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profitPerKospi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profitPerLikes',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profitPerSector1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profitPerSector2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profitPerSector3',
        ),
    ]