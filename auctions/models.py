from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ User info inherited from AbstractUser Model
    Useful fields from AbstractUser:
     User.username
     User.password """
    id = models.AutoField(primary_key=True)
    # User info inherited from AbstractUser
    watching = models.ManyToManyField('Listing')
    newalerts = models.IntegerField(default=0)
    selling_num = models.IntegerField(default=0)
    sold_num = models.IntegerField(default=0)
    earnings = models.FloatField(default=0)

    def __str__(self):
        return f"{self.username}"
    
    def dollars(self) -> str:
        """Return price formated to '$X.XX' """
        return f"{self.earnings:.2f}"
    

class Notification(models.Model):
    """Contains messages for user generated from server
    ie: listing sold, won bid, new comment, watchlist change"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=64, default="SysAdmin")
    time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user} - {self.time}"


class Category(models.Model):
    """Tags for listings"""
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.keyword}"


class Listing(models.Model):
    """Primary listing model"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=1000)
    tags = models.ManyToManyField(Category)
    imgurl = models.CharField(max_length=200, default="/static/auctions/product-placeholder.jpg")
    startbid = models.FloatField()
    price = models.FloatField(blank=True, default=0)
    winningbid = models.OneToOneField("Bid", on_delete=models.CASCADE, null=True, related_name="winning_bid_for")
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
    
    def dollars(self) -> str:
        """Return price formated to '$X.XX' """
        return f"{self.price:.2f}"


class Bid(models.Model):
    """Bids for each user, on each listing. 
    Higher bids made by user overwrite previous user's bid.
    Current winning bid recorded in listing model"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} bid {self.amount} on {self.listing}"
    
    def dollars(self) -> str:
        """Return price formated to '$X.XX' """
        return f"{self.amount:.2f}"


class Comment(models.Model):
    """Comments for each listing.
    Replyto is blank if comment is made to listing, or has username
        if made in reply to another user."""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    replyto = models.CharField(max_length=64, null=True)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.user} -> {self.listing}"
