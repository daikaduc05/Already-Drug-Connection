from .models import Users,Follow_Relations
from home.models import Post,React
from django.utils import timezone
import bcrypt
import jwt
import os
import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from home.service import HomeService
class UserService:
    def create_user(password,email):
        password_bytes = password.encode('utf-8')
        hash_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt(10))
        created_at = timezone.now()
        Users.objects.create(email = email
        ,password = hash_password.decode('utf-8')
        ,join_at = created_at)
        user = Users.objects.get(email = email)
        return user.id
    
    def follow(auth_id,user_id):
        try : 
            user = Users.objects.get(id = user_id)
            auth = Users.objects.get(id = auth_id)
            relation = Follow_Relations.objects.get(
                following = auth,
                followed = user
            )
            relation.delete()
            return "Unfollow"
        except Users.DoesNotExist :
            raise Users.DoesNotExist
        except ObjectDoesNotExist:
            content = f"{user.name} started follow you"
            HomeService.nofiticate(content=content,user_id=user_id)
            Follow_Relations.objects.create(
                following = auth,
                followed = user
            )
            return "Follow"
    def react(auth_id,post_id):
        try : 
            post = Post.objects.get(id = post_id)
            auth = Users.objects.get(id = auth_id)
            reacting = React.objects.get(
                post = post,
                user = auth
            )
            post.numoflikes -= 1
            reacting.delete()
            return "Unlike"
        except Post.DoesNotExist :
            raise Post.DoesNotExist
        except ObjectDoesNotExist:
            content = f"{auth.name} liked your post"
            post_auth = post.user
            if(post_auth.id != auth_id):
                HomeService.nofiticate(content=content,user_id=post_auth.id)
            post.numoflikes += 1
            React.objects.create(
                post = post,
                user = auth
            )
            return "Like"
    
class Authen:
    def authen_account(email,password):
        user = Users.objects.get(email = email)
        if(user.authenticate(password=password)):
            return user.id
        else:
            return None

    def gen_jwt(email):
        payload = {
            'email' : email,
        }
        token = jwt.encode(payload=payload,key=os.getenv("JWT_SECRET"),algorithm='HS256')
        return token

    def decode_jwt(token):
        try:
            decoded_payload = jwt.decode(token,os.getenv("JWT_SECRET"),algorithms=['HS256'])
            user = Users.objects.get(email = decoded_payload['email'])
            
            if user :
                return user.id
            else:
                return None
        except jwt.InvalidTokenError:
            return None
        except Users.DoesNotExist:
            raise Users.DoesNotExist

    def jwt_required(request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
            if token_type != 'Bearer':
                return JsonResponse({'message': 'Invalid token type'}, status=401)
            user_id = Authen.decode_jwt(token)
         
            if user_id is None:
                return JsonResponse({'message': 'Invalid token'}, status=401)
            data = {'message': 'ok',
                'user_id' : user_id
            }
            return data
        except ValueError:
            return None