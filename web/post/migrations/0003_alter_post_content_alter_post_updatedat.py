# Generated by Django 4.0.4 on 2022-05-04 16:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_remove_post_likeusers_post_likeusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=330),
        ),
        migrations.AlterField(
            model_name='post',
            name='updatedAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
