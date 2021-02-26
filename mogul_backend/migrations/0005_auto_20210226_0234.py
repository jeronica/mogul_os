# Generated by Django 3.1.7 on 2021-02-26 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mogul_backend', '0004_auto_20210226_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='character_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='character',
            name='corporation_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(default='Cool Guy', max_length=32, null=True),
        ),
    ]