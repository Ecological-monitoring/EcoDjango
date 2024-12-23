# Generated by Django 5.1.4 on 2024-12-23 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0009_riskassessment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskassessment',
            name='date',
            field=models.DateField(auto_now_add=True, help_text='Дата оцінки'),
        ),
        migrations.AlterField(
            model_name='riskassessment',
            name='risk_level',
            field=models.CharField(blank=True, default='Unknown', help_text='Рівень ризику', max_length=100),
            preserve_default=False,
        ),
    ]
