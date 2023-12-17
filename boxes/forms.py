from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models import F
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *


class BoxesForm(forms.ModelForm):
    clientfrom = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    clientto = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    phonefrom = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    phoneto = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    addressfrom = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    addressto = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    tarif = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'rows': 3,
        'class': 'form-control',
    }))
    amount = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    weight = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    volumesm = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    delivery = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    minsm = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    maxsm = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    discount = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
    }))
    val = (
        ('TMT', 'Manat'),
        ('USD', 'Dollar')
    )
    valuta = forms.TypedChoiceField(
        choices=val, widget=forms.Select(attrs={'class': 'form-control', }))
    toleg = (
        ('', '----------'),
        ('tolendi', 'tolendi'),
        ('tolenmedi', 'tolenmedi'),
    )
    payment = forms.TypedChoiceField(
        choices=toleg, widget=forms.Select(attrs={'class': 'form-control', }))

    boximg = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
    }))
    regionfrom = forms.ModelChoiceField(queryset=Region.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control', }))
    regionto = forms.ModelChoiceField(required=False, queryset=Region.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control', }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['payment'].initial = self.instance.payment
            self.fields['valuta'].initial = self.instance.valuta

    class Meta:
        model = Boxes
        fields = "__all__"


class RegionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegionForm, self).__init__(*args, **kwargs)
        self.fields['hi_region'] = forms.ModelChoiceField(
            queryset=Region.objects.filter(hi_region=F('name'))
        )
        self.fields['hi_region'].required = False
        self.fields['hi_region'].widget.attrs['class'] = 'form-control'
        self.fields['tarif'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Region
        fields = "__all__"


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = "__all__"


class BoxHistoryForm(forms.ModelForm):
    class Meta:
        model = BoxHistory
        fields = "__all__"


class NotificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)

        self.fields['theme'].widget.attrs['class'] = 'form-control'
        self.fields['maintxt'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Notification
        fields = "__all__"


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget.attrs['class'] = 'form-control'
        self.fields['comment'].widget.attrs['placeholder'] = 'Добавьте свое сообщение'
        self.fields['comment'].widget.attrs['style'] = 'width: max-content;'

        self.fields['answer'].widget.attrs['class'] = 'form-control'
        self.fields['answer'].widget.attrs['placeholder'] = 'Добавьте свой ответ'
        self.fields['answer'].widget.attrs['style'] = 'width: max-content'

        

    class Meta:
        model = Feedback
        fields = "__all__"


class PointForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PointForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Point
        fields = "__all__"