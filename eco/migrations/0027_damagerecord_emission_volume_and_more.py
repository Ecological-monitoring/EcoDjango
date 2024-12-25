# Generated by Django 5.1.4 on 2024-12-24 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0026_alter_pollutantdetails_hazard_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='damagerecord',
            name='emission_volume',
            field=models.FloatField(default=0.0, verbose_name='Обсяг викидів, скидів або розміщених відходів (М)'),
        ),
        migrations.AddField(
            model_name='damagerecord',
            name='region_coefficient',
            field=models.FloatField(default=1.0, verbose_name='Регіональний коефіцієнт (К₃)'),
        ),
        migrations.AddField(
            model_name='damagerecord',
            name='violation_characteristic',
            field=models.FloatField(default=1.0, verbose_name='Коефіцієнт характеру порушення (К₂)'),
        ),
        migrations.AlterField(
            model_name='damagerecord',
            name='damage_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сума збитків'),
        ),
    ]