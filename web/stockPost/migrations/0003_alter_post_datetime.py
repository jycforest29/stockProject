# Generated by Django 4.0.4 on 2022-04-18 01:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockPost', '0002_alter_post_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 18, 10, 23, 55, 978191)),
        ),
    ]
