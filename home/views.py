from django.shortcuts import render
from user.views import AuthenticatedAPIView
from rest_framework.views import APIView
from .service import HomeService
from django.http import JsonResponse
from rest_framework import status
from .serializer import PostSerializer,CommentSerializer,NofiticationSerializer,SearchedSerializer,PostDetailSerializer
from user.serializer import ProfileDetailSerializer
from rest_framework import generics
from user.models import Users
from .models import Post as aPost, Nofitication as aNofitication, React as aReact
from django.core.exceptions import ObjectDoesNotExist
from .pagination import Pagination
from django.db.models import Q
from user.service import UserService
from .models import Comment as aComment
# Create your views here.
class Comment(AuthenticatedAPIView):
    def post(self,request,format = None):
        data = request.data.copy()
        data['user'] = self.user_id
        serialize = CommentSerializer(data=data)
        try:
            post = aPost.objects.get(id = data['post'])
            post.numofcomment += 1
            messenge = f"{self.user_id} commented your post"

            user = post.user
            if(self.user_id != user.id):
                HomeService.nofiticate(user_id=user.id,content=messenge)
        except ObjectDoesNotExist:
            return JsonResponse(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if serialize.is_valid():
            serialize.save()  
            return JsonResponse(serialize.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
            
class Post(AuthenticatedAPIView):
    def post(self,request,format = None):
            data = request.data.copy()
            data['user'] = self.user_id
            serialize = PostSerializer(data=data)
            if serialize.is_valid():
                serialize.save()  
                return JsonResponse(serialize.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetail(AuthenticatedAPIView, generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = ProfileDetailSerializer
    def get(self,request,*args, **kwargs):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return super().get(request,*args, **kwargs)
    
class NewFeedView(AuthenticatedAPIView,generics.ListAPIView):
    queryset = aPost.objects.all()
    serializer_class = PostSerializer
    pagination_class = Pagination

class NofitcationView(AuthenticatedAPIView,generics.ListAPIView): 
    serializer_class = NofiticationSerializer
    def get_queryset(self):
        return aNofitication.objects.filter(user_id = self.user_id)
    pagination_class = Pagination

class SearchView(AuthenticatedAPIView,generics.ListAPIView):
    serializer_class = SearchedSerializer
    def get_queryset(self):
        user = self.request.data['user_info']
        return Users.objects.filter(Q(username__icontains = user) | Q(name__icontains = user))
    pagination_class = Pagination


class React(AuthenticatedAPIView):
    def post(self,request,format = None):
        try:
            auth_id = self.user_id
            post_id = request.data['post_id']
            action = UserService.react(auth_id=auth_id,post_id=post_id)
            data = {
                "messenge" : f" user {auth_id} {action} post {post_id} "
            }
            return JsonResponse(
                data = data,
                status = status.HTTP_200_OK
            )
        except aPost.DoesNotExist:
            data = {
                "messenge" : "User does not exist"
            }
            return JsonResponse(
                data = data,
                status = status.HTTP_404_NOT_FOUND
            )


class DeleteComment(AuthenticatedAPIView):
    def post(self,request,*args, **kwargs):
        comment = aComment.objects.get(id = request.data['comment_id'])
        if(comment.user.id != self.user_id):
            data ={
                "messenge" : "You do not have permission"
            }
            return JsonResponse(
                data=data,
                status = status.HTTP_401_UNAUTHORIZED
            )
        else:
            comment.delete()
            data ={
                "messenge" : "Deleted"
            }
            return JsonResponse(
                data=data,
                status = status.HTTP_200_OK
            )

class DeletePost(AuthenticatedAPIView):
    def post(self,request,*args, **kwargs):
        post = aPost.objects.get(id = request.data['post_id'])
        if(post.user.id != self.user_id):
            data ={
                "messenge" : "You do not have permission"
            }
            return JsonResponse(
                data=data,
                status = status.HTTP_401_UNAUTHORIZED
            )
        else:
            post.delete()
            data ={
                "messenge" : "Deleted"
            }
            return JsonResponse(
                data=data,
                status = status.HTTP_200_OK
            )
        
class PostDetail(AuthenticatedAPIView, generics.RetrieveAPIView):
     queryset = aPost.objects.all()
     serializer_class = PostDetailSerializer
     def get(self,request,*args, **kwargs):
         context = super().get_serializer_context()
         context.update({'request': self.request})
         return super().get(request,*args, **kwargs)

