from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
        
class Biding(models.Model):
    amount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='bids')

class Category(models.Model):
    categoryname = models.CharField(max_length=100, blank=True) 

    def __str__(self):
        return self.categoryname

class Listing(models.Model):
    Listingname = models.CharField(max_length=30)
    Description = models.CharField(max_length=2000)
    Startbid = models.ForeignKey(Biding, on_delete=models.CASCADE, blank=True, null=True, related_name="biding")
    Imageurl = models.CharField(max_length=2000000)
    Active = models.BooleanField(default=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")   
    
    def __str__(self):
        return self.Listingname

class Comment(models.Model):
    content = models.CharField(max_length=300)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='commentslisting')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='commentsauthor')


