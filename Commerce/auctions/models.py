from django.contrib.auth.models import AbstractUser
from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import BinaryField
from django.utils import timezone


Categories = [
    ('Clothing','Clothing' ),
    ('Technology', 'Technology'),
    ('Home Products','Home Products' ),
    ('Toys','Toys' ),
    ('Food and Beverages', 'Food and Beverages'),
    ('Other','Other')
]




class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class  Listing(models.Model):
    Title = models.CharField(max_length=45)
    Description = models.CharField(max_length=1064)
    created_time = models.DateTimeField(default = timezone.now)
    Price = models.IntegerField()
    Image = models.URLField(blank = True, default=None, null=True)
    Current_Bid = models.ForeignKey('Bids',blank= True, null=True,  related_name='current_bid', on_delete=CASCADE)
    Category = models.CharField( choices=Categories, max_length=24)
    creator = models.ForeignKey('User', on_delete=PROTECT, default=None, related_name='user_who_made_the_auction' )
    buyer = models.ForeignKey("User", null=True, related_name="buyer", on_delete=PROTECT, default=None) 
    closed = models.BooleanField(default=False)
    comments = models.ManyToManyField('Comment', blank=True, related_name='comments' )
    watchers = models.ManyToManyField('User', blank=True, related_name='watched_listing' )

    def __str__(self):
        return f"{self.Title} - {self.Price} by {self.creator} " 



class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='who_will_make_the_bid')
    Auction = models.ForeignKey('Listing', on_delete=CASCADE, related_name='auction_made_by_the_user')
    bid = models.IntegerField()
    Date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s' % (self.bid)


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_who_made_the_comment')
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s' % (self.user, self.date)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.user.username} listed {self.listing.id}"





     
     
        

