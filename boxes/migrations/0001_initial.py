# Generated by Django 4.1.7 on 2023-11-09 07:55

import boxes.models
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Boxes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputdate', models.DateTimeField(auto_now_add=True)),
                ('updatedate', models.DateTimeField(auto_now=True)),
                ('clientfrom', models.CharField(blank=True, max_length=255)),
                ('clientto', models.CharField(blank=True, max_length=255)),
                ('phonefrom', models.CharField(max_length=25)),
                ('phoneto', models.CharField(blank=True, default='', max_length=25)),
                ('addressfrom', models.CharField(blank=True, default='', max_length=255)),
                ('addressto', models.CharField(blank=True, default='', max_length=255)),
                ('tarif', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('weight', models.DecimalField(decimal_places=3, default=Decimal('0'), max_digits=20)),
                ('volumesm', models.DecimalField(decimal_places=3, default=Decimal('0'), max_digits=20)),
                ('delivery', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('minsm', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('maxsm', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('placecount', models.IntegerField(default=0)),
                ('discount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('valuta', models.CharField(choices=[('TMT', 'Manat'), ('USD', 'Dollar')], default='tmt', max_length=25)),
                ('status', models.CharField(default='create', max_length=25)),
                ('comment', models.CharField(blank=True, max_length=2500, null=True)),
                ('select', models.BooleanField(default=False)),
                ('payment', models.CharField(blank=True, choices=[('tolendi', 'tolendi'), ('tolenmedi', 'tolenmedi')], max_length=25, null=True)),
                ('boximg', models.ImageField(blank=True, default='images/emptybox.png', upload_to=boxes.models.set_image_name)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputdate', models.DateTimeField(auto_now_add=True)),
                ('theme', models.CharField(max_length=150)),
                ('maintxt', models.TextField(default='', max_length=2500)),
                ('published', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, default='images/emptybox.png', upload_to=boxes.models.set_image_name)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tarif', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('hi_region', models.CharField(blank=True, default='0', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputdate', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(default=1)),
                ('type', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='UserPoint', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputdate', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('comment', models.TextField(default='', max_length=2500)),
                ('answer', models.TextField(blank=True, default='', max_length=2500)),
                ('type', models.IntegerField(default=0)),
                ('room', models.CharField(max_length=250)),
                ('ansuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='AnswerUserFeedback', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='UserFeedback', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputdate', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('comment', models.CharField(blank=True, max_length=50)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boxes.boxes', verbose_name='Boxes')),
                ('user', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, related_name='UserCart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BoxHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputdate', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('create', 'Create'), ('called', 'Called'), ('approved', 'Approved'), ('accepted', 'Accepted'), ('sent', 'Sent'), ('rejected', 'Rejected'), ('canceled', 'Canceled'), ('closed', 'Closed')], default='create', max_length=25)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boxes.boxes', verbose_name='Boxes')),
                ('regionbh', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='H_region', to='boxes.region', verbose_name='RegionBH')),
                ('userfrom', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, related_name='UserFrom', to=settings.AUTH_USER_MODEL)),
                ('userto', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, related_name='UserTo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='boxes',
            name='regionfrom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='A_region', to='boxes.region'),
        ),
        migrations.AddField(
            model_name='boxes',
            name='regionto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='B_region', to='boxes.region'),
        ),
        migrations.AddField(
            model_name='boxes',
            name='user',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
    ]