# Generated by Django 4.1.7 on 2023-04-05 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0015_alter_region_hi_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='type_region',
        ),
        migrations.AlterField(
            model_name='region',
            name='hi_region',
            field=models.CharField(default=0, max_length=20),
        ),
    ]
