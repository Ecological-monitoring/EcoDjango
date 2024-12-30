# Generated by Django 5.1 on 2024-12-30 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0032_alter_damagerecord_damage_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthRiskAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_name', models.CharField(help_text="Назва об'єкта", max_length=100)),
                ('concentration', models.FloatField(help_text='Концентрація речовини, мг/м³')),
                ('risk_level', models.CharField(blank=True, help_text='Рівень ризику', max_length=100)),
                ('hq', models.FloatField(blank=True, help_text='Hazard Quotient (HQ)', null=True)),
                ('cr', models.FloatField(blank=True, help_text='Cancer Risk (CR)', null=True)),
                ('ladd', models.FloatField(blank=True, help_text='Lifetime Average Daily Dose (LADD), мг/(кг·день)', null=True)),
                ('date', models.DateField(auto_now_add=True, help_text='Дата оцінки')),
                ('pollutant', models.ForeignKey(help_text='Забруднююча речовина', on_delete=django.db.models.deletion.CASCADE, to='eco.pollutant')),
            ],
        ),
        migrations.DeleteModel(
            name='RiskAssessment',
        ),
    ]