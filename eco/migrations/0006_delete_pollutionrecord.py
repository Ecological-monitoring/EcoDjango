# Generated by Django 5.1.4 on 2024-12-19 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0005_emissionrecord_delete_example_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PollutionRecord',
        ),
    ]