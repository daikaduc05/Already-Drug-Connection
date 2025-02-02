from django.db import models
import bcrypt
# Create your models here.

class Users(models.Model):
    
    name = models.CharField(max_length=75,null=True)
    username = models.CharField(max_length=75,null=True)
    email = models.EmailField(max_length=75,unique=True)
    avt_url = models.URLField(null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.BooleanField(null=True)
    password = models.CharField(max_length=75)
    join_at = models.DateField()
    graduate = models.CharField(max_length=75,null=True)
    reletion_ship = models.CharField(max_length=75,null=True)
    live_in = models.CharField(max_length=75,null=True)
    from_to = models.CharField(max_length=75,null=True)
   
    def __str__(self):
        return self.username
    def authenticate(self,password):
        password_bytes = password.encode('utf-8')
        hashpass = self.password.encode('utf-8')
        if bcrypt.checkpw(password_bytes,hashpass) :
            return self
        else:
            return None
        
class Follow_Relations(models.Model):
    following = models.ForeignKey(Users, related_name='followings', on_delete=models.CASCADE)
    followed = models.ForeignKey(Users, related_name='followers', on_delete=models.CASCADE)
    
# user.follower.following