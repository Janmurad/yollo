from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

import jwt
import datetime
import uuid

from yoldatm.settings import SECRET_KEY
from .models import Cuser
from boxes.models import Region


def getGroup(groups):
    for gr in groups:
        return gr.name


def generate_jwt_token(token_type, exp_time, user_id):
    iat = datetime.datetime.now()
    exp = iat + datetime.timedelta(minutes=exp_time)
    encoded_token = jwt.encode({
        "token_type": token_type,
        "exp": int(exp.timestamp()),
        "iat": int(iat.timestamp()),
        "jti": str(uuid.uuid4()),
        "user_id": user_id
    }, SECRET_KEY, algorithm="HS256")
    return encoded_token


def get_cuser_and_region(user):
    cuser = Cuser.objects.get(user=user)
    cuser.block = 0 # type: ignore
    cuser.save()
    region = Region.objects.get(pk=cuser.region_id) # type: ignore
    return cuser, region


def create_response(refresh_token, access_token, user_data, address_data):
    return Response({
        'refresh': refresh_token,
        'access': access_token,
        'user': user_data,
        'address': address_data
    })


def auth_response(request, username, password):
    user = authenticate(username=username, password=password)

    if user:
        login(request, user)

        refresh_token = generate_jwt_token("refresh", 10000, user.id) # type: ignore
        access_token = generate_jwt_token("access", 10, user.id) # type: ignore

        cuser, region = get_cuser_and_region(user)

        return create_response(
            refresh_token,
            access_token,
            {'username': user.username, 'name': cuser.name, # type: ignore
             'email': user.email, 'phone': cuser.phone, 'type': cuser.type_user}, # type: ignore
            {'address': cuser.address, 'region_name': region.name,
             'region_id': cuser.region_id, 'region_hi': region.hi_region} # type: ignore
        )
    else:
        return Response({'detail': 'Username or password error', 'code': 'user_or_pass_error', 'messages': [
            {'message': 'Username or password error'}]})


class CuserAPIList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cusers = Cuser.objects.filter(
            Q(type_user='driver') | Q(type_user='manager')).values()
        return Response({'users': cusers})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        gr = getGroup(request.user.groups.all())
        if(gr == 'client'):
            user = request.user
            user.groups.clear()
            user.delete()
        return Response({'message': "Logout successful"})
    

class ChangePasswordView(generics.UpdateAPIView):
    # permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        return Response({'message': "Password changed"})


class UserAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cuser = Cuser.objects.get(user=request.user)
        user = User.objects.get(username=request.user)
        region = Region.objects.get(pk=cuser.region_id) # type: ignore

        return Response({
            "user": {'username': user.username, "name": cuser.name, 'email': user.email, 'phone': cuser.phone, 'type': cuser.type_user},
            "address": {'address': cuser.address, 'region_name': region.name, 
                        'region_id': cuser.region_id, 'region_hi': region.hi_region} # type: ignore
            })

    def put(self, request):
        cuser = Cuser.objects.get(user=request.user)
        user = User.objects.get(username=request.user)
        region = Region.objects.get(pk=cuser.region_id) # type: ignore
        try:
            user.email = request.data['email']
            user.first_name = request.data['name']
            ps = request.data.get('password', None)
            if ps != None:
                user.set_password(request.data['password'])
            user.save()
            cuser.name = request.data['name']
            cuser.address = request.data['address']
            cuser.phone = request.data['phone']
            cuser.region = Region.objects.get(pk=request.data['region_id'])
            cuser.save()
        except Exception as ex:
            return Response({'detail': str(ex), 'code': 'profil_update', 'messages': [{'message': str(ex) + ' field is required'}]})
        
        region = Region.objects.get(pk=request.data['region_id'])

        return Response({
            "user": {'username': user.username, "name": cuser.name, 'email': user.email, 'phone': cuser.phone, 'type': cuser.type_user},
            "address": {'address': cuser.address, 'region_name': region.name, 
                        'region_id': cuser.region_id, 'region_hi': region.hi_region} # type: ignore
            })


class CreateUserAPI(APIView):
    def post(self, request):
        phone = request.data['phone']
        password = request.data['password']

        user_exists = User.objects.filter(username=phone).exists()

        if not user_exists:
            user = User.objects.create_user(
                username=phone,
                email=phone + '@mail.com',
                password=password,
                first_name=request.data['name']
            )

            user_created = User.objects.get(username=phone)

            client_group = Group.objects.get(name='client')
            user_created.groups.add(client_group)
            user_created.is_staff = True
            user_created.save()

        else:
            user_created = User.objects.get(username=phone)

        cuser_exists = Cuser.objects.filter(user=user_created).exists()

        if not cuser_exists:
            try:
                region = Region.objects.get(pk=request.data['region_city'])
                cuser = Cuser.create(
                    user=user_created,
                    phone=phone,
                    name=request.data['name'],
                    type_user='client',
                    region=region,
                    address=request.data['address']
                )
                cuser.save()
            except Exception as ex:
                print("-----" + str(ex))
        
        return auth_response(request, phone, password)


class MyObtainTokenPairView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.method == 'POST':
            username = request.data['username'].lower()
            password = request.data['password']
            return auth_response(request, username, password)
