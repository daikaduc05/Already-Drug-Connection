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
from .views import Register,Login,Follow,UserProfileDetail,EditProfile
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
 
    path('register',Register.as_view(),name='Register'),
    path('login',Login.as_view(),name = 'Login'),
    path('follow',Follow.as_view(),name = 'Follow'),
    path('profile/<int:pk>',UserProfileDetail.as_view(),name='Profile'),
    path('edit/profile',EditProfile.as_view(),name="Edit Profile")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
