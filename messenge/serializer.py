from rest_framework import serializers
import re
from Common.regex import remail,rpassword
from Common.messenge import WRONG_FORM_EMAIL,WRONG_FORM_PASSWORD
from .models import Messenge,ChatBox
from home.serializer import PostSerializer
from home.pagination import Pagination

class MessengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messenge
        fields = "__all__"

class ChatBoxDetailSerializer(serializers.ModelSerializer):
    messenge = serializers.SerializerMethodField()
    class Meta:
        model = ChatBox
        fields = ["is_block","messenge","user1","user2"]
    
    def get_messenge(self,obj):
        request = self.context.get('request')
        queryset = obj.messenge.all().order_by('id')
        paginator = Pagination()
        messenge_queryset = queryset  
        messenge_queryset.update(seen=1)
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = MessengerSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data).data

class ChatBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBox
        fields = "__all__"