# Generated by Django 3.1.8 on 2021-04-12 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mogul_backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('context_id', models.IntegerField(null=True)),
                ('context_id_type', models.CharField(max_length=64, null=True)),
                ('date', models.DateTimeField()),
                ('description', models.CharField(max_length=128)),
                ('first_party_id', models.BigIntegerField()),
                ('ref_id', models.BigIntegerField()),
                ('reason', models.CharField(max_length=64)),
                ('ref_type', models.CharField(max_length=64)),
                ('second_part_id', models.BigIntegerField()),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('tax_receiver_id', models.BigIntegerField()),
                ('user', models.ForeignKey(blank=True, help_text='The user to whom this journal belongs.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
