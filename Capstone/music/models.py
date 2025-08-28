from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL



Albumss = [
    ('Rock','Rock' ),
    ('Pop', 'Pop'),
    ('Hip Hop','Hip Hop' ),
    ('Jazz','Jazz' ),
    ('Electro', 'Electro'),
    ('90s', '90s'),
    ('Classical', 'Classical'),
    ('Funk', 'Funk'),
    ('Bollywood', 'Bollywood'),
    ('Other','Other')
]


class User(AbstractUser):
    pass

class Songs(models.Model):
    Title = models.CharField(max_length=45)
    Singer = models.CharField(max_length=105)
    Audio = models.FileField(upload_to='documents/')
    Poster = models.ForeignKey('User', on_delete=PROTECT, default=None )
    Albums = models.CharField( choices=Albumss, max_length=24, default="Other")
    liked_by = models.ManyToManyField('User', default=None, blank=True, related_name='song_likers')
    class Meta:
        db_table='Songs'
