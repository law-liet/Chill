from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=64)
    is_chilled = models.BooleanField(default=False)
    friends = models.ManyToManyField("self")
    events = models.ManyToManyField(Event)
    joined_event = models.ForeignKey(Event)

class Event(models.Model):
    chiller = models.ForeignKey(User, related_name="chiller")
    members = models.ManyToManyField(User, related_name="members")
    name = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    size = models.IntegerField(default=2)
    description = models.CharField(max_length=8192)