from django.shortcuts import render 
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from ..models import Listing, User


@login_required
def viewuser(request):
    return render(request, 'auctions/user/viewuser.html', {
        'user': request.user
    })


@login_required
def userlistings(request):
    return render(request, 'auctions/user/listings.html', {
        'user_listings': Listing.objects.filter(seller=request.user.id)
    })



@login_required
def userbids(request):
    pass 


@login_required
def usercomments(request):
    pass