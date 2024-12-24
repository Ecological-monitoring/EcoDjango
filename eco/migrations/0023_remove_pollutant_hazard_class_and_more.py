# Generated by Django 5.1.4 on 2024-12-24 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0022_alter_pollutant_hazard_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollutant',
            name='hazard_class',
        ),
        migrations.RemoveField(
            model_name='pollutant',
            name='hazard_coefficient',
        ),
        migrations.RemoveField(
            model_name='pollutant',
            name='kn',
        ),
        migrations.RemoveField(
            model_name='pollutant',
            name='mpc',
        ),
        migrations.RemoveField(
            model_name='pollutant',
            name='rfc',
        ),
        migrations.RemoveField(
            model_name='pollutant',
            name='sf',
        ),
        migrations.RemoveField(
            model_name='pollutant',
            name='specific_emissions',
        ),
        migrations.RemoveField(
            model_name='pollutant',
            name='tax_rate',
        ),
        migrations.AddField(
            model_name='pollutant',
            name='description',
            field=models.TextField(blank=True, help_text='Опис забруднюючої речовини', null=True),
        ),
        migrations.AlterField(
            model_name='pollutant',
            name='name',
            field=models.CharField(help_text='Назва забруднюючої речовини', max_length=100),
        ),
        migrations.AlterField(
            model_name='pollutantdetails',
            name='hazard_class',
            field=models.CharField(choices=[('I', 'І клас (надзвичайно небезпечні)'), ('II', 'ІІ клас (високонебезпечні)'), ('III', 'ІІІ клас (помірно небезпечні)'), ('IV', 'IV клас (малонебезпечні)')], default='IV', max_length=50, verbose_name='Клас небезпеки'),
        ),
        migrations.AlterModelTable(
            name='pollutant',
            table='eco_pollutant',
        ),
    ]
