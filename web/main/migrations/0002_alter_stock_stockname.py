# Generated by Django 4.0.4 on 2022-04-19 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='stockName',
            field=models.CharField(max_length=100),
        ),
    ]