from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, F, Subquery
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage

from .models import *
from .serializer import *
from users.models import Cuser


class RegionAPIList(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsAuthenticated, )


class RegionHi(generics.ListAPIView):
    queryset = Region.objects.filter(hi_region=F('name')).values()
    serializer_class = RegionSerializer


class RegionCity(generics.ListAPIView):    
    serializer_class = RegionSerializer
    #
    def get_queryset(self):
        queryset = Region.objects.exclude(hi_region=F('name'))
        region_hi = self.request.query_params.get('region_hi') # type: ignore
        print(region_hi)
        if region_hi is not None:
            queryset = queryset.filter(hi_region=region_hi)
        return queryset


def getGroup(groups):
    for gr in groups:
        return gr.name


class BoxHistoryAPIList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        boxid = Boxes.objects.filter(id=pk)
        boxhist = BoxHistory.objects.filter(box=boxid[0].pk).values('box_id','inputdate','regionbh__name','status')
        return Response({'box': BoxCustomSerializer(boxid, many=True).data[0], 'history': boxhist})

    def post(self, request, pk):
        try:
            box = Boxes.objects.get(id=pk)
            cuser = Cuser.objects.get(user=request.data['userto'])
            region = Region.objects.get(id=request.data['regionbh'])
            gr = getGroup(request.user.groups.all())
            if gr != 'client':
                box_hist = BoxHistory.objects.filter(box=box, status=request.data['status'])
                if box_hist.count() == 0:
                    box_hist = BoxHistory.objects.create(
                        box = box,
                        userfrom = request.user,
                        userto = cuser.user,
                        regionbh = region,
                        status = request.data['status']
                    )
                else:
                # print(box_hist.latest('pk').pk)
                    box_hist = BoxHistory.objects.get(id=box_hist.latest('pk').pk)
                    box_hist.userfrom = request.user
                    box_hist.userto = cuser.user # type: ignore
                    box_hist.regionbh = region
                    box_hist.status = request.data['status']
                    box_hist.save()

                box.status = request.data['status']
                box.save()
            boxs = Boxes.objects.filter(id=pk)
            box_hist = BoxHistory.objects.filter(box=box).values('box_id','inputdate','regionbh__name','status')
            return Response({'box': BoxCustomSerializer(boxs, many=True).data[0], 'history': box_hist})
        except Exception as ex:
            return Response({'detail': str(ex), 'code': 'box_create_error', 'messages': [{'message': str(ex)}]})


class BoxesAPIList(APIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = Paginator

    def get(self, request, *args, **kwargs):
        gr = getGroup(request.user.groups.all())

        cuser = Cuser.objects.get(user=request.user)

        if(gr == 'client'):
            boxes = Boxes.objects.filter(
                user=request.user).order_by('-id')
        elif(gr == 'manager'):
            boxes = Boxes.objects.filter(Q(regionfrom=cuser.region) |
                                         Q(regionto=cuser.region)).order_by('-id')
        elif(gr == 'driver' or gr == 'wdriver'):
            boxhis = BoxHistory.objects.filter(Q(userfrom=request.user) | Q(userto=request.user)).values('box')
            boxes = Boxes.objects.filter(Q(pk__in=Subquery(boxhis)) | Q(user=request.user))
        else:
            boxes = Boxes.objects.all().order_by('-id')

        pk = self.kwargs.get('pk')
        if pk != None:
            try:
                box = Boxes.objects.get(pk=pk)
                boxes = Boxes.objects.filter(pk=pk)
                boxhistory = BoxHistory.objects.filter(box=box.pk).values('box_id','inputdate','regionbh__name','status')
                return Response({'box': BoxCustomSerializer(boxes, many=True).data[0], 'history': boxhistory})
                
            except Boxes.DoesNotExist:
                raise Http404('No box with this pk exists')
        

        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('size', 10)
        paginator = self.pagination_class(boxes, page_size)
        try:
            page = paginator.page(page_number)
            return Response({'boxes': BoxCustomSerializer(page, many=True).data})
        except EmptyPage:
            return Response({'boxes': []})

        #return Response({'boxes': BoxCustomSerializer(page, many=True).data})

    def post(self, request):
        try:                
            cuser = Cuser.objects.get(user=request.user)

            if request.data['phonefrom'] == '':
                return Response({'phonefrom': 'Requiered field.'})

            if request.data['regionfrom'] == '':
                regionfrom = cuser.region
            else:
                regionfrom = Region.objects.get(pk=request.data['regionfrom'])

            if request.data['regionto'] == '':
                regionto = None
            else:
                if(request.data['regionto'] == '0'):
                    regionto = None
                else:
                    regionto = Region.objects.get(pk=request.data['regionto'])

            if request.data['clientfrom'] == '':
                clientfrom = cuser.name
            else:
                clientfrom = request.data['clientfrom']

            new_box = Boxes.objects.create(
                clientfrom=clientfrom,
                clientto=request.data['clientto'],
                phonefrom=request.data['phonefrom'],
                phoneto=request.data['phoneto'],
                addressfrom=request.data['addressfrom'],
                addressto=request.data['addressto'],
                tarif=request.data['tarif'],
                amount=request.data['amount'],
                weight=request.data['weight'],
                volumesm=request.data['volumesm'],
                delivery=request.data['delivery'],
                minsm=request.data['minsm'],
                maxsm=request.data['maxsm'],
                placecount=request.data['placecount'],
                discount=request.data['discount'],
                valuta=request.data['valuta'],
                status=request.data['status'],
                comment=request.data['comment'],
                payment=request.data['payment'],
                boximg=request.FILES.get('boximg', "images/emptybox.png"),
                regionfrom=regionfrom,
                regionto=regionto,
                user=request.user,
            )
            box = Boxes.objects.filter(pk=new_box.pk)
            BoxHistory.objects.create(
                box = new_box,
                userfrom = request.user,
                userto = cuser.user,
                regionbh = regionfrom,
                status = request.data['status']
            )
            boxhistory = BoxHistory.objects.filter(box=new_box.pk).values('box_id','inputdate','regionbh__name','status')
            return Response({'box':BoxCustomSerializer(box, many=True).data[0], 'history': boxhistory})
        except Exception as ex:
            return Response({'detail': str(ex), 'code': 'box_create_error', 'messages': [{'message': str(ex)}]})

    def put(self, request, pk):
        gr = getGroup(request.user.groups.all())

        if (gr != 'wdriver'):
            try:
                cuser = Cuser.objects.get(user=request.user)

                if request.data['phonefrom'] == '':
                    return Response({'phonefrom': 'phonefrom Requiered field.'})

                new_box = Boxes.objects.get(pk=pk)
                # new_box.clientfrom=clientfrom
                new_box.clientto=request.data['clientto']
                new_box.phonefrom=request.data['phonefrom']
                new_box.phoneto=request.data['phoneto']
                new_box.addressfrom=request.data['addressfrom']
                new_box.addressto=request.data['addressto']
                new_box.tarif=request.data['tarif']
                new_box.amount=request.data['amount']
                new_box.weight=request.data['weight']
                new_box.volumesm=request.data['volumesm']
                new_box.delivery=request.data['delivery']
                new_box.minsm=request.data['minsm']
                new_box.maxsm=request.data['maxsm']
                new_box.placecount=request.data['placecount']
                new_box.discount=request.data['discount']
                new_box.valuta=request.data['valuta']
                new_box.status=request.data['status']
                new_box.comment=request.data['comment']
                new_box.payment=request.data['payment']
                new_box.boximg=request.FILES.get('boximg', new_box.boximg)
            # new_box.user=request.user

                if request.data['regionfrom'] == '':
                    regionfrom = cuser.region
                else:
                    regionfrom = Region.objects.get(pk=request.data['regionfrom'])

                if request.data['regionto'] == '':
                    regionto = None
                else:
                    regionto = Region.objects.get(pk=request.data['regionto'])

                new_box.regionfrom=regionfrom # type: ignore
                new_box.regionto=regionto # type: ignore 

                new_box.save()
                box = Boxes.objects.filter(pk=new_box.pk)
                return Response({'box':BoxCustomSerializer(box, many=True).data[0]})
            except Exception as ex:
                return Response({'detail': str(ex), 'code': 'box_put_error', 'messages': [{'message': str(ex)}]}, status=406)
        else:
            return Response({
                'detail': 'Do not have permission for change', 'code': 'user_permission', 
                'messages': [{'message': 'Do not have permission for change'}]}, status=403)


class BoxReject(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request, pk):
        try:
            cuser = Cuser.objects.get(user=request.user)
            new_box = Boxes.objects.get(pk=pk)
            new_box.status=request.data['status']
            new_box.comment=request.data['comment']
            new_box.save()
            box = Boxes.objects.filter(pk=new_box.pk)
            return Response({'box':BoxCustomSerializer(box, many=True).data[0]})
        except Exception as ex:
            return Response({'detail': str(ex), 'code': 'box_put_comment_error', 'messages': [{'message': str(ex)}]}, status=403)


class NotificationList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notification = Notification.objects.all().order_by('-id')
        pk = self.kwargs.get('pk')
        if pk != None:
            try:
                notification = notification.filter(pk=pk)
                return Response({'notifications': NotificationSerializer(notification, many=True).data[0]})
            except Feedback.DoesNotExist:
                raise Http404('No box with this pk exists')

        return Response({'notifications': NotificationSerializer(notification, many=True).data})

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk == None:
            notification = Notification.objects.create(
                user=request.user, 
                room=uuid.uuid4(), 
                answer='', 
                comment=request.data['message']
            )
            notifi = NotificationSerializer(notification)
            return Response(notifi.data[0])


class FeedbackAPIList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        gr = getGroup(request.user.groups.all())
        cuser = Cuser.objects.get(user=request.user)

        if(gr == 'client'):
            feedback = Feedback.objects.filter(user=request.user)
        elif(gr == 'manager'):
            regions = Region.objects.filter(hi_region=(cuser.region.hi_region)) # type: ignore
            cusers = Cuser.objects.filter(region__in=regions).values('user')
            feedback = Feedback.objects.filter(user__in=cusers)
        elif(gr == 'driver'):
            feedback = Feedback.objects.filter(Q(user=request.user) | Q(ansuser=request.user))
        else:
            feedback = Feedback.objects.all().order_by('-id')

        pk = self.kwargs.get('pk')
        if pk != None:
            try:
                feedback = feedback.filter(pk=pk)
            except Feedback.DoesNotExist:
                raise Http404('No box with this pk exists')

        return Response({'feedbacks': FeedbackSerializer(feedback, many=True).data})
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk == None:
            feedback = Feedback.objects.create(user=request.user, answer='', comment=request.data['message'])
            feed = FeedbackSerializer(feedback)
            return Response(feed.data)
        else:
            try:
                feedback = Feedback.objects.get(pk=pk)
                feedback.answer = request.data['message']
                feedback.ansuser = request.user
                feedback.answerdate = datetime.now()
                feedback.save()
                feed = FeedbackSerializer(feedback)
                return Response(feed.data)
            except Feedback.DoesNotExist:
                raise Http404('No box with this pk exists')


class RegionCreate(APIView):
    def post(self, request):
        regions = Region.objects.filter(name=request.data['name']).exists()
        if(regions):
            return Response({'message': request.data['name'] + ' region is exists'})
        else:
            Region.objects.create(name=request.data['name'], tarif=50, hi_region=request.data['hi_region'])
            return Response({'message': request.data['name'] + ' region is added'})
