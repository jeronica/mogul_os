# Generated by Django 3.1.8 on 2021-04-12 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mogul_backend', '0003_auto_20210412_1156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='journal',
            old_name='second_part_id',
            new_name='second_party_id',
        ),
    ]