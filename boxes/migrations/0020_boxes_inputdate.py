# Generated by Django 4.1.7 on 2023-05-03 15:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0019_remove_boxes_inputdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxes',
            name='inputdate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
