# Generated by Django 3.1.8 on 2021-04-12 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mogul_backend', '0004_auto_20210412_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='reason',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='ref_type',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='tax_receiver_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
