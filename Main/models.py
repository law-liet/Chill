from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    fb_token = models.CharField(max_length=128)
    fb_id = models.CharField(max_length = 64)
    email = models.CharField(max_length=64)
    is_chilled = models.BooleanField(default=False)
    Type = models.CharField(default="Chilled", max_length=128)
    friends = models.ManyToManyField("self")

    def switch_chilled(self):
        self.is_chilled = not self.is_chilled
        self.save()

class Message(models.Model):
    sender = models.ForeignKey(User)
    name = models.CharField(max_length=64)
    content = models.CharField(max_length=8192)
    time = models.DateTimeField()

class Group(models.Model):
    chiller = models.ForeignKey(User, related_name="chiller")
    members = models.ManyToManyField(User, related_name="members")
    #start_time = models.DateTimeField()
    #end_time = models.DateTimeField()
    #max_size = models.IntegerField(default=2)
    #size = models.IntegerField(default=1)
    Type = models.CharField(max_length=8192)
    messages = models.ManyToManyField(Message, related_name="messages")



