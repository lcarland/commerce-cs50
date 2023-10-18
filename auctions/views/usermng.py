from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..models import User, Listing, Bid, Comment, Notification


@login_required
def viewuser(request):
    return render(request, 'auctions/user/viewuser.html', {
        'user': request.user
    })


@login_required
def userlistings(request):
    return render(request, 'auctions/user/listings.html', {
        'user_listings': Listing.objects.filter(seller=request.user.id, sold=False),
        'sold_listings': Listing.objects.filter(seller=request.user.id, sold=True)
    })


@require_http_methods(['GET', 'POST'])
@login_required
def watchlist(request):
    user = request.user
    
    if request.method == 'POST':
        id = request.POST["id"]
        user.watching.add(Listing.objects.get(id=id))
        return HttpResponseRedirect(f"{reverse('viewlisting')}?id={id}")
    
    return render(request, "auctions/user/watchlist.html", {
        'watchlist': user.watching.all()
    })


@login_required
def userbids(request):
    return render(request, "auctions/user/bids.html", {
        'bids': Bid.objects.filter(user=request.user)
    })


@login_required
def usercomments(request):
    return render(request, "auctions/user/comments.html", {
        'comments': Comment.objects.filter(user=request.user)
    })


@login_required
def postcomment(request):
    user = request.user
    listing = Listing.objects.get(id=request.POST["id"])
    content = request.POST["content"]

    new_comment = Comment.objects.create(user=user, listing=listing, content=content)
    new_comment.save()

    return HttpResponseRedirect(f"{reverse('viewlisting')}?id={listing.id}")


@require_http_methods(['POST'])
@login_required
def rmv_from_watch(request):
    listing = Listing.objects.get(id=request.POST["id"])
    user = request.user
    user.watching.remove(listing)
    return HttpResponseRedirect(f"{reverse('viewlisting')}?id={listing.id}")


@login_required
def inbox(request):
    return render(request, 'auctions/user/notifications.html', {
        'notifications': Notification.objects.filter(user=request.user).order_by("-time")
    })


@login_required
def get_alerts(request):
    user = request.user
    alerts = user.newalerts
    user.newalerts = 0
    user.save()
    return JsonResponse({
        'num': alerts
    })


def make_notification(sender:str, receiver:User, content:str):
    newMSG = Notification.objects.create(user=receiver, sender=sender, message=content)
    receiver.newalerts += 1
    newMSG.save()
    receiver.save()