# Generated by Django 5.1.4 on 2024-12-23 12:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0008_alter_taxrate_pollutant_alter_taxrate_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_name', models.CharField(help_text="Назва об'єкта", max_length=100)),
                ('concentration', models.FloatField(help_text='Концентрація речовини, мг/м³')),
                ('risk_level', models.CharField(blank=True, help_text='Рівень ризику', max_length=50, null=True)),
                ('date', models.DateField(auto_now_add=True, help_text='Дата оцінки ризику')),
                ('pollutant', models.ForeignKey(help_text='Забруднююча речовина', on_delete=django.db.models.deletion.CASCADE, to='eco.pollutant')),
            ],
        ),
    ]