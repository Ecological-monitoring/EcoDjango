# Generated by Django 5.1.4 on 2024-12-19 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0004_taxrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmissionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_name', models.CharField(help_text="Назва об'єкта", max_length=100)),
                ('volume', models.FloatField(help_text="Об'єм викидів у тоннах")),
                ('date', models.DateField(help_text='Дата викиду')),
            ],
        ),
        migrations.DeleteModel(
            name='example',
        ),
        migrations.AlterField(
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
            model_name='pollutionrecord',
            name='date',
            field=models.DateField(help_text='Дата викиду'),
        ),
        migrations.AlterField(
            model_name='pollutionrecord',
            name='object_name',
            field=models.CharField(help_text="Назва об'єкта", max_length=100),
        ),
        migrations.AlterField(
            model_name='pollutionrecord',
            name='pollutant',
            field=models.ForeignKey(help_text='Забруднююча речовина', on_delete=django.db.models.deletion.CASCADE, to='eco.pollutant'),
        ),
        migrations.AlterField(
            model_name='pollutionrecord',
            name='volume',
            field=models.FloatField(help_text="Об'єм викидів у тоннах"),
        ),
        migrations.AlterField(
            model_name='taxrate',
            name='pollutant',
            field=models.ForeignKey(help_text='Забруднююча речовина', on_delete=django.db.models.deletion.CASCADE, to='eco.pollutant'),
        ),
        migrations.AlterField(
            model_name='taxrate',
            name='rate',
            field=models.FloatField(help_text='Ставка податку за 1 тонну (грн)'),
        ),
        migrations.AddField(
            model_name='emissionrecord',
            name='pollutant',
            field=models.ForeignKey(help_text='Забруднююча речовина', on_delete=django.db.models.deletion.CASCADE, to='eco.pollutant'),
        ),
    ]