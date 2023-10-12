from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    # User info inherited from AbstractUser
    watching = models.ManyToManyField('Listing', blank=True, null=True)
    selling_num = models.IntegerField(default=0)
    sold_num = models.IntegerField(default=0)
    earnings = models.FloatField(default=0)

    def __str__(self):
        return self.username

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user} - {self.time}"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=64)

    def __str__(self):
        return self.keyword


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=1000)
    tags = models.ManyToManyField(Category)
    imgurl = models.CharField(max_length=200, null=True, default="/static/auctions/product-placeholder.jpg")
    startbid = models.FloatField()
    price = models.FloatField(blank=True, default=0)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} bid {self.amount} on {self.listing}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    replyto = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.listing}"
