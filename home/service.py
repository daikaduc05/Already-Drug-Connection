from .models import Nofitication,Post
from user.models import Users
from django.utils import timezone
import bcrypt
import jwt
import os
import json
from django.http import JsonResponse
from .models import Post
from django.core.exceptions import ObjectDoesNotExist

class HomeService:
    def nofiticate(content,user_id):
        user = Users.objects.get(id = user_id)
        Nofitication.objects.create(
            user = user,
            content = content,
            create_at = timezone.now()
        ) 
        
        
    