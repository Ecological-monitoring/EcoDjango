# Generated by Django 5.1.4 on 2024-12-20 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0003_remove_emissionrecord_volume_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emissionrecord',
            name='pollutant',
        ),
        migrations.AddField(
            model_name='emissionrecord',
            name='pollutant_name',
            field=models.CharField(default=0, max_length=255, verbose_name='Забруднююча речовина'),
            preserve_default=False,
        ),
    ]
