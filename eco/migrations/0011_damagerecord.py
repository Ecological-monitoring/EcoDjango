# Generated by Django 5.1.4 on 2024-12-23 22:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0010_alter_riskassessment_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DamageRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_name', models.CharField(max_length=255, verbose_name="Назва об'єкта")),
                ('year', models.IntegerField(verbose_name='Рік')),
                ('damage_type', models.CharField(choices=[('Air', 'Викиди в атмосферу'), ('Water', 'Скиди у водні об’єкти')], max_length=255, verbose_name='Тип завданої шкоди')),
                ('damage_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сума збитків')),
                ('pollutant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eco.pollutant', verbose_name='Забруднююча речовина')),
            ],
        ),
    ]