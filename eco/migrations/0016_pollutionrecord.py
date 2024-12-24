# Generated by Django 5.1.4 on 2024-12-24 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0015_remove_taxcalculation_tax_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollutionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('value', models.FloatField()),
                ('substance', models.CharField(choices=[('Оксид вуглецю', 'Оксид вуглецю'), ('Речовини у вигляді суспендованих твердих частинок', 'Речовини у вигляді суспендованих твердих частинок'), ('Діоксид азоту', 'Діоксид азоту'), ('Аміак', 'Аміак'), ('Сірки діоксид', 'Сірки діоксид'), ('Метан', 'Метан')], max_length=255)),
            ],
        ),
    ]
