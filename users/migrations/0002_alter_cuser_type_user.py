# Generated by Django 4.1.7 on 2023-12-10 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuser',
            name='type_user',
            field=models.CharField(choices=[('driver', 'Driver'), ('wdriver', 'RegionDriver'), ('manager', 'Manager'), ('admin', 'Admin'), ('client', 'Client')], default='client', max_length=10),
        ),
    ]
