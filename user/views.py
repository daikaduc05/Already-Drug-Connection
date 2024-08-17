from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegisterSerializer,ProfileDetailSerializer,EditProfileSerializer
from .service import UserService,Authen
from rest_framework import status
from .models import Users
from django.db import IntegrityError
from django.http import JsonResponse
from Common.messenge import INTERGRITY_EMAIL
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import generics
from functools import wraps

class AuthenticatedAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        try:
            jwt_data = Authen.jwt_required(request)
            if not jwt_data:
                return JsonResponse({'messenge': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            self.user_id = jwt_data.get('user_id')
            if not self.user_id:
                return JsonResponse({'messenge': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            return super().dispatch(request, *args, **kwargs) 
        except Users.DoesNotExist:
            return JsonResponse({'messenge' : "Wrong authentication"},status = status.HTTP_401_UNAUTHORIZED)
    
class Register(APIView):
    def post(self,request,format = None):
        try:
            serialize = RegisterSerializer(data = request.data)
            if(serialize.is_valid()):  
                id = UserService.create_user(request.data['password'],
                request.data['email']
                )   
                data ={
                    "user id" : id,
                    "messenge" : "created"
                }
                return JsonResponse(data,status = status.HTTP_201_CREATED)
            else:
                return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
                return Response(INTERGRITY_EMAIL,status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request,format = None):
        email = request.data['email']
        password = request.data['password']
        try:
            if Authen.authen_account(email=email,password=password):
                token = Authen.gen_jwt(email=email)       
                data = {
                    "user id" : Authen.authen_account(email=email,password=password),
                    "token" : token,
                    "messenge" : "login successful"
                }
                return JsonResponse(data=data
                    ,status = status.HTTP_200_OK
                )
            else:
                data = {
                    "messenge" : "fail"
                }
                return JsonResponse(
                    data=data
                    ,status = status.HTTP_401_UNAUTHORIZED
                )
        except ObjectDoesNotExist:
            data = {
                "messenge" : "account does not exist"
            }
            return JsonResponse(
                data=data,
                status = status.HTTP_401_UNAUTHORIZED
            )
class Follow(AuthenticatedAPIView):
    def post(self,request,format = None):
        try:
            auth_id = self.user_id
            user_id = request.data['user_id']
            action = UserService.follow(auth_id=auth_id,user_id=user_id)
            data = {
                "messenge" : f"{auth_id} {action} {user_id}"
            }
            return JsonResponse(
                data = data,
                status = status.HTTP_200_OK
            )
        except Users.DoesNotExist:
            data = {
                "messenge" : "User does not exist"
            }
            return JsonResponse(
                data = data,
                status = status.HTTP_404_NOT_FOUND
            )

class UserProfileDetail(AuthenticatedAPIView, generics.RetrieveAPIView):
    
    queryset = Users.objects.all()
    serializer_class = ProfileDetailSerializer
    def get(self,request,*args, **kwargs):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return super().get(request,*args, **kwargs)
    
class EditProfile(AuthenticatedAPIView):
    def post(self,request,*args, **kwargs):
        data = request.data.copy()
        user = Users.objects.get(id = self.user_id)
        serialize = EditProfileSerializer(user,data = data,partial = True)
        if serialize.is_valid():
            serialize.save()
            return JsonResponse(serialize.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
