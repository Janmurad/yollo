# Generated by Django 4.1.7 on 2023-12-11 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boxes', '0003_alter_boxes_user_alter_boxhistory_userfrom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxes',
            name='user',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
        migrations.AlterField(
            model_name='boxhistory',
            name='userfrom',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UserFrom', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='boxhistory',
            name='userto',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UserTo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UserCart', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='ansuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AnswerUserFeedback', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UserFeedback', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='point',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UserPoint', to=settings.AUTH_USER_MODEL),
        ),
    ]
