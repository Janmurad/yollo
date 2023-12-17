from django.db import models
from django.contrib.auth.models import User
import uuid, decimal


class Region(models.Model):
    region_type = (
        ('AG', 'Aşgabat'),
        ('AH', 'Ahal'),
        ('BN', 'Balkan'),
        ('MR', 'Mary'),
        ('LB', 'Lebap'),
        ('DZ', 'Daşoguz'),
    )
    name = models.CharField(max_length=50)
    tarif = models.DecimalField(max_digits=20, decimal_places=2, default=decimal.Decimal(0.0))
    hi_region = models.CharField(max_length=50, default='0', blank=True)
    # type_region = models.CharField(max_length=10, choices=region_type, 
        # verbose_name="Region district")ll

    def __str__(self) -> str:
        return self.name


def set_image_name(instance, filename):
    if filename == "":
        return "images/emptybox.png"

    ext = filename.split('.')[-1]
    return "images/{0}.{1}".format(uuid.uuid4(), ext)


class Boxes(models.Model):
    val = (
        ('TMT', 'Manat'),
        ('USD', 'Dollar')
    )
    toleg = (
        ('tolendi', 'tolendi'),
        ('tolenmedi', 'tolenmedi'),
    )
    inputdate = models.DateTimeField(auto_now_add=True)
    updatedate = models.DateTimeField(auto_now=True)
    clientfrom = models.CharField(max_length=255, blank=True)
    clientto = models.CharField(max_length=255, blank=True)
    phonefrom = models.CharField(max_length=25)
    phoneto = models.CharField(max_length=25, default="", blank=True)
    addressfrom = models.CharField(max_length=255, default="", blank=True)
    addressto = models.CharField(max_length=255, default="", blank=True)
    tarif = models.DecimalField(max_digits=20, decimal_places=2, default=decimal.Decimal(0.0)) 
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=decimal.Decimal(0.0)) 
    weight = models.DecimalField(max_digits=20, decimal_places=3, default=decimal.Decimal(0.0)) 

    volumesm = models.DecimalField(max_digits=20, decimal_places=3, default=decimal.Decimal(0.0)) 
    delivery = models.DecimalField(max_digits=20, decimal_places=2, default=decimal.Decimal(0.0)) 
    minsm = models.DecimalField(max_digits=20, decimal_places=2, default=decimal.Decimal(0.0)) 
    maxsm = models.DecimalField(max_digits=20, decimal_places=2, default=decimal.Decimal(0.0)) 

    placecount = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=decimal.Decimal(0.0)) 
    valuta = models.CharField(max_length=25, choices=val, default="tmt")
    status = models.CharField(max_length=25, default="create")
    comment = models.CharField(max_length=2500, null=True, blank=True)
    select = models.BooleanField(default=False)
    payment = models.CharField(max_length=25, choices=toleg, null=True, blank=True)
    boximg = models.ImageField(
        upload_to=set_image_name, default="images/emptybox.png", blank=True)
    regionfrom = models.ForeignKey('Region', related_name="A_region", on_delete=models.PROTECT, null=True)
    regionto = models.ForeignKey(
        'Region', related_name="B_region", on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Users',
                             on_delete=models.SET_NULL, blank=True, default=1, null=True) # type: ignore

    def __str__(self) -> str:
        return self.phonefrom


class BoxHistory(models.Model):
    stats = (
        ('create', 'Create'),
        ('called', 'Called'),
        ('approved', 'Approved'),
        ('accepted', 'Accepted'),
        ('sent', 'Sent'),
        ('rejected', 'Rejected'),
        ('canceled', 'Canceled'),
        ('closed', 'Closed')
    )
    box = models.ForeignKey('Boxes', verbose_name='Boxes', on_delete=models.CASCADE)
    inputdate = models.DateTimeField(auto_now=True)
    userfrom = models.ForeignKey(User, related_name="UserFrom", on_delete=models.SET_NULL, blank=True, default=1, null=True) # type: ignore
    userto = models.ForeignKey(User, related_name="UserTo", on_delete=models.SET_NULL, blank=True, default=1, null=True) # type: ignore
    regionbh = models.ForeignKey(Region, related_name="H_region", verbose_name="RegionBH", on_delete=models.PROTECT,default=0) # type: ignore
    status = models.CharField(max_length=25, choices=stats, default="create")

    def __str__(self) -> str:
        return self.status + " - " + str(self.inputdate)
    

class Cart(models.Model):
    inputdate = models.DateTimeField(auto_now_add=True)
    box = models.ForeignKey('Boxes', verbose_name='Boxes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="UserCart", on_delete=models.SET_NULL, blank=True, default=1, null=True) # type: ignore
    status = models.IntegerField(default=0)
    comment = models.CharField(max_length=50, blank=True)


class Notification(models.Model):
    inputdate = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(max_length=150)
    maintxt = models.TextField(max_length=2500, default='')
    published = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=set_image_name, default="images/emptybox.png", blank=True)


class Feedback(models.Model):
    inputdate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="UserFeedback", on_delete=models.SET_NULL, null=True)
    ansuser = models.ForeignKey(User, related_name="AnswerUserFeedback", on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(max_length=2500, default="")
    answer = models.TextField(max_length=2500, default="", blank=True)
    answerdate = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.comment + " - " + str(self.inputdate)


class Point(models.Model):
    inputdate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="UserPoint", on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(default=1)
    type = models.IntegerField(default=0)
