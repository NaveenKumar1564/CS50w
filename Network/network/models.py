from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.utils import timezone


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="following")


class Post(models.Model):

    creator =  models.ForeignKey('User', on_delete=PROTECT, default=None, related_name='post_creator' )
    Description = models.CharField(max_length=1064)
    timestamp = models.DateTimeField(default = timezone.now)
    liked_by = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.Post,
            "Description": self.Description,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "like": self.like,
        }


    


