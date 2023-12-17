from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from boxes.models import Region


class Cuser(models.Model):
    user_type = (
        ('driver', 'Driver'),
        ('wdriver', 'RegionDriver'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    user = models.ForeignKey(User, verbose_name='Users', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=25, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    inputdate = models.DateTimeField(auto_now=True)
    datefrom = models.DateTimeField(auto_now=True, blank=True)
    dateto = models.DateTimeField(auto_now=True, blank=True)
    type_user = models.CharField(max_length=10, choices=user_type, default='client')
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True) # type: ignore

    @classmethod
    def create(cls, user, phone, name, type_user, region, address):
        cuser = cls.objects.create(
            user=user, phone=phone, name=name, type_user=type_user, region=region, address=address,
            datefrom=datetime.now(), dateto=datetime.now())
        cuser.save(force_insert=True)
        return cuser

    def __str__(self) -> str:
        return self.name

