# Generated by Django 4.0.4 on 2022-04-20 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='likeUsers',
        ),
    ]
