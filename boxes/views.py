from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q, Subquery
from django.core.paginator import Paginator

from .forms import *
from .models import *
from users.models import Cuser
from users.forms import DashboardForm


@login_required(login_url='login')
def create_box(request):

    if request.method == "POST":
        forms = BoxesForm(request.POST, request.FILES)
        if forms.is_valid():
            try:
                forms.save()
                cuser = Cuser.objects.get(user=request.user)
                region = Region.objects.get(pk=request.POST['regionfrom'])
                cuser.region = region
                cuser.save()
                return redirect('boxeslist')
            except:
                print('hello')

    else:
        forms = BoxesForm(initial={'user': request.user})

    context = {'form': forms, 'activ': 'boxes', 'activ': 'boxes'}
    return render(request, 'boxes/form.html', context)


def getGroup(groups):
    for gr in groups:
        return gr.name


@login_required(login_url='login')
def boxeslist(request):
    gr = getGroup(request.user.groups.all())

    cuser = Cuser.objects.get(user=request.user)

    if(gr == 'client'):
        boxes = Boxes.objects.filter(user=request.user)
    elif(gr == 'manager'):
        boxes = Boxes.objects.filter(
            Q(regionfrom=cuser.region) | Q(regionto=cuser.region))
    elif(gr == 'driver'):
        boxhis = BoxHistory.objects.filter(
            Q(userfrom=request.user) | Q(userto=request.user)
        ).values('box')
        boxes = Boxes.objects.filter(
            Q(pk__in=Subquery(boxhis)) | Q(user=request.user)
        )
    else:
        boxes = Boxes.objects.all()

    if 'datefrom' not in request.session:
        request.session['datefrom'] = datetime.today().astimezone(
            timezone.utc).strftime('%Y-%m-01')

    if 'dateto' not in request.session:
        request.session['dateto'] = datetime.today().astimezone(
            timezone.utc).strftime('%Y-%m-%d') + " 23:59:59"

    if 'clientfrom' not in request.session:
        request.session['clientfrom'] = ''

    if 'clientto' not in request.session:
        request.session['clientto'] = ''

    if 'phonefrom' not in request.session:
        request.session['phonefrom'] = ''

    if 'phoneto' not in request.session:
        request.session['phoneto'] = ''

    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            request.session['datefrom'] = str(form.cleaned_data['datefrom'])
            request.session['dateto'] = str(form.cleaned_data['dateto']) + " 23:59:59"
            request.session['clientfrom'] = form.cleaned_data['clientfrom']
            request.session['clientto'] = form.cleaned_data['clientto']
            request.session['phonefrom'] = form.cleaned_data['phonefrom']
            request.session['phoneto'] = form.cleaned_data['phoneto']
    else:
        form = DashboardForm(initial={
            'datefrom': request.session['datefrom'], 'dateto': request.session['dateto'],
            'clientfrom': request.session['clientfrom'], 'clientto': request.session['clientto'],
        })

    if 'clientfrom' not in request.session:
        request.session['clientfrom'] = ''

    boxes = boxes.filter(clientfrom__contains=request.session['clientfrom'])
    boxes = boxes.filter(phonefrom__contains=request.session['phonefrom'])
    boxes = boxes.filter(clientto__contains=request.session['clientto'])
    boxes = boxes.filter(phoneto__contains=request.session['phoneto'])
    boxes = boxes.filter(
        inputdate__gte=request.session['datefrom'], inputdate__lte=request.session['dateto'])

    paginator = Paginator(boxes.order_by('-id'), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    print(request.session['dateto'])
    context = {
        'boxes': boxes, 'activ': 'boxes', 'form': form, 'page_obj': page_obj, 'cuser': cuser,
    }
    return render(request, 'boxes/index.html', context)


@login_required(login_url='login')
def boxesstatus(request, status):
    gr = getGroup(request.user.groups.all())

    cuser = Cuser.objects.get(user=request.user)

    if(gr == 'client'):
        boxes = Boxes.objects.filter(user=request.user)
    elif(gr == 'manager'):
        boxes = Boxes.objects.filter(
            Q(regionfrom=cuser.region) | Q(regionto=cuser.region))
    elif(gr == 'driver'):
        boxhis = BoxHistory.objects.filter(
            Q(userfrom=request.user) | Q(userto=request.user)
        ).values('box')
        boxes = Boxes.objects.filter(
            Q(pk__in=Subquery(boxhis)) | Q(user=request.user)
        )
    else:
        boxes = Boxes.objects.all()

    form = DashboardForm()
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        boxes = boxes.filter(clientfrom__contains=request.POST['clientfrom'])
        boxes = boxes.filter(phonefrom__contains=request.POST['phonefrom'])
        boxes = boxes.filter(clientto__contains=request.POST['clientto'])
        boxes = boxes.filter(phoneto__contains=request.POST['phoneto'])

    boxes = boxes.filter(status=status).order_by('-id')

    paginator = Paginator(boxes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'boxes': boxes, 'activ': 'boxes', 'form': form, 'page_obj': page_obj, 'cuser': cuser,
    }
    return render(request, 'boxes/index.html', context)


def box_select(request, pk):

    box = Boxes.objects.get(pk=pk)
    box.select = not box.select
    box.save()

    try:
        cart = Cart.objects.get(user=request.user, box=box)
        if(box.select):
            cart.user = request.user
            cart.box = box
            cart.status = 0
            cart.save()
        else:
            cart.delete()
    except Cart.DoesNotExist:
        cart = Cart(user=request.user, box=box)
        cart.save()
    except Cart.MultipleObjectsReturned:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def box_view(request, pk):
    box = Boxes.objects.get(id=pk)
    boxhist = BoxHistory.objects.filter(box=box)

    context = {'activ': 'boxes', 'box': box, 'boxhist': boxhist}
    return render(request, 'boxes/view.html', context)


def box_update(request, pk):
    box = Boxes.objects.get(id=pk)

    if request.method == "POST":
        forms = BoxesForm(request.POST, request.FILES, instance=box)
        # print(request.POST)
        if forms.is_valid():
            # print('step1')
            try:
                forms.save()
                return redirect('boxeslist')
            except Exception as ex:
                print(str(ex))
        else:
            print(forms.errors.as_data())

    else:
        forms = BoxesForm(instance=box)
    # form = BoxesForm(instance=box)
    context = {'box': box, 'form': forms}
    return render(request, 'boxes/update.html', context)


def box_selected_send(request):
    cart = Cart.objects.filter(user=request.user, status=0)
    cuserlist = Cuser.objects.exclude(type_user='client')
    if request.method == "POST":
        cuser = Cuser.objects.get(user=request.POST['userto'])
        if(((request.user != cuser.user) and (request.POST['status'] != '0') and (request.POST['userto'] != '0')) or (request.POST['status'] == 'approved')
           or (request.POST['status'] == 'accepted')):
            for cartbox in cart:
                box = cartbox.box
                box.status = request.POST['status']
                box.select = False
                box.save()

                boxhis = BoxHistory(
                    box=box,
                    userfrom=request.user,
                    userto=cuser.user,
                    regionbh=cuser.region,
                    status=request.POST['status'],
                )
                boxhis.save()
                cartbox.status = 1
                cartbox.save()
            return redirect('boxeslist')
        # elif((request.POST['status'] != '0') or (request.POST['userto'] != '0')):

    context = {'activ': 'boxes', 'cart': cart, 'cuserlist': cuserlist}
    return render(request, 'boxes/selected.html', context)


def box_fromto(request, pk):
    box = Boxes.objects.get(id=pk)
    boxhist = BoxHistory.objects.filter(box=box)

    if request.method == "POST":
        form_copy = request.POST.copy()
        cuser = Cuser.objects.get(user=request.POST['userto'])
        form_copy['regionbh'] = cuser.region
        form_copy['box'] = box
        form_copy['userfrom'] = request.user
        request.POST = form_copy
        form = BoxHistoryForm(request.POST)

        if form.is_valid():
            # print('men barde')
            form.save()
            box.status = request.POST['status']
            box.save()
            return redirect('/yolloadmin/api/box/boxeslist')

    else:
        form = BoxHistoryForm()

    context = {'activ': 'boxes', 'box': box, 'form': form, 'boxhist': boxhist}
    return render(request, 'boxes/fromto.html', context)


def region_index(request):

    if request.method == 'GET':
        regions = Region.objects.all()
        return render(request, 'region/index.html', {'regions': regions, 'activ': 'region'})


def region_update(request, pk):
    region = Region.objects.get(pk=pk)

    if request.method == 'POST':
        form = RegionForm(request.POST, instance=region)
        if form.is_valid():
            form.save()
            return redirect('/yolloadmin/api/box/region/index')
    else:
        form = RegionForm(instance=region)

    context = {
        'activ': 'region', 'form': form
    }
    return render(request, 'region/update.html', context)


def region_form(request):

    if request.method == 'POST':
        # form = RegionForm(request.POST, request.FILES)
        form = RegionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/yolloadmin/api/box/region/index')
    else:
        form = RegionForm()
    return render(request, 'region/form.html', {'form': form, 'activ': 'region'})


def success(request):
    return HttpResponse('successfully uploaded')


@login_required(login_url='login')
def notification_index(request):

    notification = Notification.objects.all()
    context = {'activ': 'notification', 'notification': notification}
    return render(request, 'notification/index.html', context)


@login_required(login_url='login')
def notification_form(request):

    if request.method == 'POST':
        form = NotificationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('notification')
    else:
        form = NotificationForm()

    context = {
        'activ': 'notification', 'form': form
    }
    return render(request, 'notification/form.html', context)


def notification_update(request, pk):
    note = Notification.objects.get(pk=pk)

    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notification')
    else:
        form = NotificationForm(instance=note)

    context = {
        'activ': 'notification', 'form': form
    }
    return render(request, 'notification/update.html', context)


@login_required(login_url='login')
def feedback_index(request):

    gr = getGroup(request.user.groups.all())

    cuser = Cuser.objects.get(user=request.user)

    if(gr == 'client'):
        feedback = Feedback.objects.filter(user=request.user)
    elif(gr == 'manager'):
        regions = Region.objects.filter(hi_region=(cuser.region.hi_region)) # type: ignore
        cusers = Cuser.objects.filter(region__in=regions).values('user')
        feedback = Feedback.objects.filter(user__in=cusers) 

    elif(gr == 'driver'):
        feedback = Feedback.objects.filter(
            Q(user=request.user) | Q(ansuser=request.user)
        )
    else:
        feedback = Feedback.objects.all()

    feedback = feedback.order_by('-id')

    paginator = Paginator(feedback, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'activ': 'feedback', 'page_obj': page_obj}
    return render(request, 'feedback/index.html', context)


@login_required(login_url='login')
def feedback_form(request):

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback')
    else:
        form = FeedbackForm(initial={
            'user': request.user, 'room': uuid.uuid4(), 'answer': ''
        })

    context = {
        'activ': 'feedback', 'form': form
    }
    return render(request, 'feedback/form.html', context)


@login_required(login_url='login')
def feedback_answer(request, pk):

    feed = Feedback.objects.get(pk=pk)

    if request.method == 'POST':
        form_copy = request.POST.copy()
        form_copy['ansuser'] = request.user
        form_copy['status'] = 1
        request.POST = form_copy
        form = FeedbackForm(request.POST, instance=feed)
        if form.is_valid():
            form.save()
            return redirect('feedback')
    else:
        form = FeedbackForm(instance=feed)

    context = {
        'activ': 'feedback', 'form': form
    }
    return render(request, 'feedback/answer.html', context)