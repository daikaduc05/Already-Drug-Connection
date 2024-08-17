from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from user.views import AuthenticatedAPIView
from .models import ChatBox,Messenge as aMessenge
from .serializer import ChatBoxDetailSerializer,ChatBoxSerializer
from home.pagination import Pagination
from django.http import JsonResponse
class Messenge(AuthenticatedAPIView):
    def post(self,request,*args, **kwargs):
        chatbox = ChatBox.objects.get(id = request.data['id'])
        content = request.data['content']
        from_user = self.user_id
        to_user = request.data['to_user']
        mess = aMessenge.objects.create(
            chat_box = chatbox,
            content = content,
            from_user = from_user,
            to_user = to_user
        )
        mess.save()

class ChatBoxDetail(AuthenticatedAPIView,generics.RetrieveAPIView):
    queryset = ChatBox.objects.all()
    serializer_class = ChatBoxDetailSerializer
    def get(self,request,*args, **kwargs):

        context = super().get_serializer_context()
        context.update({'request': self.request})
        return super().get(request,*args, **kwargs)

class ChatBoxList(AuthenticatedAPIView,generics.ListAPIView):
    queryset = ChatBox.objects.all()
    serializer_class = ChatBoxSerializer 
    pagination_class = Pagination

class FirstMessenge(AuthenticatedAPIView):
    def post(self,request,*args, **kwargs):
        chat = ChatBox.objects.create()
        chat.save()
        data = {
            "chat_id" : chat.id,
            "from_user" : self.user_id,
            "to_user" : request.data['user_id']
        }
        return JsonResponse(
            data=data
        )
