# Generated by Django 5.1.4 on 2024-12-19 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0003_alter_pollutionrecord_pollutant'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(help_text='Ставка податку за 1 тонну')),
                ('pollutant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eco.pollutant')),
            ],
        ),
    ]
