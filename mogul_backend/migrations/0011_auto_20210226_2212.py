# Generated by Django 3.1.7 on 2021-02-26 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mogul_backend', '0010_auto_20210226_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='station_name',
            field=models.CharField(default='Unknown', max_length=64),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type_name',
            field=models.CharField(default='Unknown', max_length=64),
        ),
    ]