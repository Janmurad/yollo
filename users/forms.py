from django import forms
import datetime
from boxes.models import Region
from .models import Cuser
from django.contrib.auth.models import User


class DashboardForm(forms.Form):
    datefrom = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
        })
    )
    dateto = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'margin: 1rem, 0, 1rem, 0;'
        })
    )

    clientfrom = forms.CharField(required=False ,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'Клиент отправитель'
    }))
    clientto = forms.CharField(required=False ,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'Клиент получатель'
    }))

    phonefrom = forms.CharField(required=False ,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'Телефон отправителья'
    }))
    phoneto = forms.CharField(required=False ,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'Телефон получателья'
    }))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password'
    }))


class UpdateCUserForm(forms.Form):
    types = (
        ('', '----------'),
        ('driver', 'Driver'),
        ('wdriver', 'RegionDriver'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
    }))
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phonenumber',
    }))
    user_type = forms.ChoiceField(
        choices=types,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )


class CuserModelForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
        
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
    }))
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phonenumber',
    }))
    user_types = (
        ('driver', 'Driver'),
        ('wdriver', 'RegionDriver'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    type_user = forms.ChoiceField(
        choices=user_types,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Cuser
        fields = ['name', 'address', 'region', 'phone', 'type_user']


class CuserForm(forms.Form):
    types = (
        ('', '----------'),
        ('driver', 'Driver'),
        ('wdriver', 'RegionDriver'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
    }))
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phonenumber',
    }))
    user_type = forms.ChoiceField(
        choices=types,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password'
    }))


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phonenumber',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password'
    }))
    repassword = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Re-password',
        'type': 'password'
    }))
