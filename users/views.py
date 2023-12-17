from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignUpForm, CuserForm, UpdateCUserForm,CuserModelForm
from .models import Cuser
from boxes.models import Region
from yoldatm.views import getGroup

from datetime import datetime


@login_required(login_url='login')
def cuser_list(request):
    gr = getGroup(request.user.groups.all())
    # print(gr)
    if(gr == 'admin'):
        cusers = Cuser.objects.exclude(type_user='client')
    elif(gr == 'manager'):        
        cusers = Cuser.objects.exclude(type_user='client')
    elif(gr == 'driver'):        
        cusers = Cuser.objects.exclude(user=request.user)
    else:
        cusers = Cuser.objects.filter(user=request.user).exclude(type_user='client')

    cusers = cusers.exclude(type_user='admin')

    context = {'cusers': cusers, 'activ': 'cuser'}
    return render(request, 'users/index.html', context)

@login_required(login_url='login')
def cuser_view(request, pk):

    cusers = Cuser.objects.get(pk=pk)

    context = {'cusers': cusers, 'activ': 'cuser'}
    return render(request, 'users/view.html', context)

@login_required(login_url='login')
def cuser_update(request, pk):
    
    cusers = Cuser.objects.get(pk=pk)
    user = cusers.user
    form= CuserModelForm(instance=cusers)
    if request.method == 'POST':
        form = CuserModelForm(request.POST, instance=cusers)
        if form.is_valid():
            
            if form.save():
                my_group = Group.objects.get(name=form.cleaned_data['type_user'])
                user.groups.clear()
                user.groups.add(my_group)
                user.save()
                return redirect('cuserlist')
            else:
                print('not save')
            
    else:
        pass #form= CuserForm(instance=cusers)
    context = {'cusers': cusers, 'form': form , 'activ': 'cuser'}
    return render(request, 'users/update.html', context)


@login_required(login_url='login')
def client_list(request):
    gr = getGroup(request.user.groups.all())
    if(gr == 'admin'):
        cusers = Cuser.objects.filter(type_user='client').exclude(user=None)
    elif(gr == 'manager'):
        cusers = Cuser.objects.filter(type_user='client').exclude(user=None)
    elif(gr == 'client'):
        cusers = Cuser.objects.filter(user=request.user).exclude(user=None)
    else:
        cusers = Cuser.objects.filter(type_user='client').exclude(user=None)

    context = {'cusers': cusers, 'activ': 'client'}
    return render(request, 'users/client.html', context)


@login_required(login_url='login')
def create_user(request):
    if request.method == 'POST':
        form = CuserForm(request.POST)

        user = User.objects.filter(username=request.POST['username']).exists()
        if not (user):
            user = User.objects.create_user(username=request.POST['username'],
                email=request.POST['username']+'@mail.com', password=request.POST['password'])

        user_created = User.objects.get(username=request.POST['username'])
        my_group = Group.objects.get(name=request.POST['user_type'])
        user_created.groups.add(my_group)
        user_created.is_staff = True
        user_created.save()

        cuser = Cuser.objects.filter(user=user_created).exists()
        if not (cuser):
            try:
                region = Region.objects.get(pk=request.POST['region'])
                cuser= Cuser.create(user=user_created, phone=request.POST['phone'],
                    name=request.POST['name'], type_user=request.POST['user_type'],
                    region=region, address=request.POST['address'])
                cuser.save()
                
            except Exception as ex:
                print(str(ex))
            return redirect('cuserlist')
        else:
            print('Olar yaly cuser bar uje')

    else:
        form= CuserForm()
    context= {'form': form, 'activ': 'cuser'}
    return render(request, 'users/create.html', context)


def login_page(request):
    forms= LoginForm()
    message = ""
    if request.method == 'POST':
        forms= LoginForm(request.POST)
        if forms.is_valid():
            username= forms.cleaned_data['username'].lower()
            password= forms.cleaned_data['password']
            user= authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                message = "password"
    context= {'form': forms, 'message': message}
    # print('login')
    return render(request, 'users/login.html', context)


def signup_page(request):

    if request.method == 'POST':
        forms= SignUpForm(request.POST)
        username = request.POST['username'].lower()
        cuser= Cuser.objects.filter(name=username).exists()
        user= User.objects.filter(username=username).exists()
        if not (user):
            user= User.objects.create_user(username=username,
                email=username+'@mail.com', password=request.POST['password'])

        user_created= User.objects.get(username=username)
        my_group = Group.objects.get(name='client')
        user_created.groups.add(my_group)
        user_created.is_staff= True
        user_created.save()

        cuser= Cuser.objects.filter(user=user_created).exists()
        if not (cuser):
            try:
                region= Region.objects.get(pk=1)
                cuser= Cuser.create(user=user_created, phone=request.POST['phone'],
                    name=request.POST['username'], type_user='client',
                    region=region, address=request.POST['address'])
                # print("çuser created")
                cuser.save()
                # print('cuser saved')
            except Exception as ex:
                print(str(ex))
        return redirect('login')
    else:
        forms= SignUpForm()

    # print("signup")
    context= {'form': forms}
    return render(request, 'users/signup.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')
