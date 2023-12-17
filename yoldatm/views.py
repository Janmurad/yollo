from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime, timezone
from django.core.paginator import Paginator
from boxes.models import Boxes, BoxHistory, Region
from users.models import Cuser
from django.db.models import Q, Subquery
from users.forms import DashboardForm

def getGroup(groups):
    for gr in groups:
        return gr.name


@login_required(login_url='login')
def dashboard(request):
    gr = getGroup(request.user.groups.all())
    
    try:
        cuser = Cuser.objects.get(user=request.user)
    except Cuser.DoesNotExist:
        try:
            cuser= Cuser.create(user=request.user, phone='phone',
                    name=request.user, type_user='client',
                    region=None)
            cuser.save()
        except:
            cuser = Cuser.objects.get(user=request.user)        

    datefrom = datetime.today().astimezone(timezone.utc).strftime('%Y-%m-01')
    dateto = datetime.today().astimezone(timezone.utc).strftime('%Y-%m-%d')
    form= DashboardForm(initial={'datefrom':datefrom, 'dateto': dateto})
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        datefrom = request.POST['datefrom']
        dateto = request.POST['dateto']

    dateto = dateto + " 23:59:59"

    if(gr == 'client'):
        boxes = Boxes.objects.filter(user=request.user).order_by('-id')
    elif(gr == 'manager'):
        boxes = Boxes.objects.filter(
            Q(regionfrom=cuser.region) | Q(regionto=cuser.region)
            ).filter(
                # Q(inputdate=datefrom) & Q(inputdate=dateto)
                inputdate__range=(datefrom, dateto) 
            ).order_by('-id')
    elif(gr == 'driver'):
        boxhis = BoxHistory.objects.filter(
            Q(userfrom=request.user) | Q(userto=request.user)
        ).values('box')
        boxes = Boxes.objects.filter(
            Q(pk__in=Subquery(boxhis)) | Q(user=request.user)
            ).order_by('-id')
    else:
        boxes = Boxes.objects.all().order_by('-id')

    paginator = Paginator(boxes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'boxes': boxes, 'activ': 'dashboard', 'form': form, 'page_obj': page_obj
    }
    return render(request, 'dashboard.html', context)
