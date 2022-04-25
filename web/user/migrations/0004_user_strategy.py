# Generated by Django 4.0.4 on 2022-04-23 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_user_profit'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='strategy',
            field=models.CharField(choices=[('안전형', '안전형'), ('중립형', '중립형'), ('위험형', '위험형')], default='안전형', max_length=3),
        ),
    ]