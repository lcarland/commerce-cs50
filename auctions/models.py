from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    # User info inherited from AbstractUser
    watching = models.ForeignKey('Listing', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=64)

    def __str__(self):
        return self.keyword


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    tags = models.ManyToManyField(Category)
    imgurl = models.CharField(max_length=200, blank=True, null=True)
    startbid = models.FloatField()

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
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user} -> {self.listing}"
