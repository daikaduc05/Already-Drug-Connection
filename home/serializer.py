from rest_framework import serializers
import re
from Common.regex import remail,rpassword
from Common.messenge import WRONG_FORM_EMAIL,WRONG_FORM_PASSWORD
from .models import Post,Comment,Nofitication,React
from user.models import Users
from .pagination import Pagination
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        user = serializers.PrimaryKeyRelatedField(queryset=Users)
        fields = '__all__'
    

class SearchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','name','username']
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        user = serializers.PrimaryKeyRelatedField(queryset=Users)
        post = serializers.PrimaryKeyRelatedField(queryset=Post)
        fields = '__all__'
class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        user = serializers.PrimaryKeyRelatedField(queryset=Users)
        post = serializers.PrimaryKeyRelatedField(queryset=Post)
        fields = '__all__'

class NofiticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nofitication
        fields = '__all__'

    
class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    reacts = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['comments','reacts','numofcomment','numofreact']

    def get_comments(self, obj):
        request = self.context.get('request')
        queryset = obj.comments.all().order_by('id')
        paginator = Pagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = CommentSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data).data
    
    def get_reacts(self, obj):
        request = self.context.get('request')
        queryset = obj.reacts.all().order_by('id')
        paginator = Pagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ReactSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data).data
    
   
        
    
