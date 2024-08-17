"""
URL configuration for Meetbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import Post,Comment,UserProfileDetail,NewFeedView,NofitcationView,SearchView,React,DeleteComment,DeletePost,PostDetail

urlpatterns = [
 
    path('post',Post.as_view(),name='Post'),
    path('comment',Comment.as_view(),name='Comment'),
    path('home',NewFeedView.as_view(),name="Home"),
    path('nofitication',NofitcationView.as_view(),name = "Nofitication"),
    path('search',SearchView.as_view(),name="Search"),
    path('react',React.as_view(),name="React"),
    path('deletepost',DeletePost.as_view(),name='Delete Post'),
    path('deletecomment',DeleteComment.as_view(),name='Delete Comment'),
    path('postdetail/<int:pk>',PostDetail.as_view(),name="Post Detail")
    
] 
