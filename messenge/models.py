from django.db import models
from user.models import Users
# Create your models here.


class ChatBox(models.Model):
    user1 = models.ForeignKey(Users,related_name="box_as_1",on_delete=models.CASCADE)
    user2 = models.ForeignKey(Users,related_name="box_as_2",on_delete=models.CASCADE)
    is_block = models.BooleanField()

class UserChatBox(models.Model):
    chat_box = models.ForeignKey(ChatBox,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,related_name="chat_box",on_delete=models.CASCADE)
class Messenge(models.Model):
    chat_box = models.ForeignKey(ChatBox,related_name="messenge",on_delete=models.CASCADE)
    from_user = models.ForeignKey(Users,related_name="send_mess",on_delete=models.CASCADE)
    to_user = models.ForeignKey(Users,related_name="received_mess",on_delete=models.CASCADE)
    content = models.TextField()
    seen = models.BooleanField(default=0)