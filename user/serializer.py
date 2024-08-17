from rest_framework import serializers
import re
from Common.regex import remail,rpassword
from Common.messenge import WRONG_FORM_EMAIL,WRONG_FORM_PASSWORD
from .models import Users,Follow_Relations
from home.serializer import PostSerializer
from home.pagination import Pagination
class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow_Relations
        fields = ['followed']
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow_Relations
        fields = ['following']
        
class RegisterSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)  
    
    def validate(self, data):
        if not re.match(remail,data['email']) :
            raise serializers.ValidationError(WRONG_FORM_EMAIL)
        elif not re.match(rpassword,data['password']):
            raise serializers.ValidationError(WRONG_FORM_PASSWORD)
        return data

class ProfileDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()
    class Meta:
        model = Users
        fields = ['posts','followers','followings']

    def get_posts(self, obj):
        request = self.context.get('request')
        queryset = obj.posts.all().order_by('id')
        paginator = Pagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = PostSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data).data
    
    def get_followers(self, obj):
        request = self.context.get('request')
        queryset = obj.followers.all().order_by('id')
        paginator = Pagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = FollowerSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data).data
    
    def get_followings(self, obj):
        request = self.context.get('request')
        queryset = obj.followings.all().order_by('id')
        paginator = Pagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = FollowingSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data).data

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(EditProfileSerializer,self).__init__(*args, **kwargs)
        self.fields.pop('password')