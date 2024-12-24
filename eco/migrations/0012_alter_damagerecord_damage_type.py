# Generated by Django 5.1.4 on 2024-12-24 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0011_damagerecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='damagerecord',
            name='damage_type',
            field=models.CharField(choices=[('Air', 'Викиди в атмосферу'), ('Water', 'Скиди у водні об’єкти'), ('Soil', 'Забруднення ґрунту')], max_length=255, verbose_name='Тип завданої шкоди'),
        ),
    ]
