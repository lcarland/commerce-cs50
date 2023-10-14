from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from ..models import Listing, Category, Bid


def viewlisting(request):
    listing = validate_listing_query(request)
    return render(request, 'auctions/viewlisting.html', {
        'listing': listing
    })


@login_required
def createlisting(request):
    message: str = ""

    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        tags = request.POST["tags"] # type str -> list
        imgurl = request.POST["imgurl"]
        startbid: float = request.POST["startbid"]
        seller_id = request.user

        tags = tags.split(',')

        try:
            listing = Listing.objects.create(title=title, description=description, imgurl=imgurl, seller=seller_id, price=startbid, startbid=startbid)
            listing.save()

            for val in tags:
                val = val.strip()
                if not val:
                    continue
                tag, was_created = Category.objects.get_or_create(keyword=val)

            listing.tags.add(tag)

        except IntegrityError:
            render(request, 'auctions/createlisting.html', {
                'message': "Error submitting listing"
            })
        
        message = "Listing posted"


    return render(request, 'auctions/createlisting.html', {
        'message' : message
    })

@login_required
def listing_operation(request):
    user = request.user
    list_id = request.GET.get('id', '0')
    operation = request.GET.get('oper')
    listing = Listing.objects.get(id=list_id)

    if not listing:
        return invalidoperation(request, 'Ivalid Listing Provided')
    if listing.seller != user:
        return invalidoperation(request, 'This Listing does not belong to you!')

    if operation == 'accept':
        listing.sold = True
        listing.save()
        user.earnings += listing.price 
        user.save()
    elif operation == 'close':
        listing.delete()
    elif operation == 'edit':
        tag_objs = Category.objects.filter(listings__id=user.id)
        tags = [obj.keyword for obj in tag_objs]

        return render(request, 'auctions/createlisting.html', {
            'message': '',
            'newlisting': False,
            'id': listing.id,
            'title': listing.title,
            'description': listing.description,
            'tags': ', '.join(map(str, tags)),
            'imgurl': listing.imgurl
        }) 
    else:
        pass
    return HttpResponseRedirect(reverse("viewuser"))


@login_required
def updatelisting(request):
    listing = Listing.objects.get(id=request.GET.get('id'))
    user = request.user

    if not listing:
        return invalidoperation(request, 'Ivalid Listing Provided')
    
    option = request.GET.get('oper')

    if option == 'edit':
        if listing.seller != user:
            return invalidoperation(request, 'This Listing does not belong to you!')
        
        listing.title = request.POST["title"]
        listing.description = request.POST["description"]
        listing.imgurl = request.POST["imgurl"]

        tags = request.POST["tags"] # type str -> list
        tags = tags.split(',')

        try:
            listing.save()

            for val in tags:
                val = val.strip()
                if not val:
                    continue
                tag, was_created = Category.objects.get_or_create(keyword=val)

            listing.tags.add(tag)

        except IntegrityError:
            render(request, 'auctions/createlisting.html', {
                'message': "Error submitting listing"
            })

    elif option == 'placebid':
        if listing.seller == user:
            return invalidoperation(request, 'You cannot place a bid on your own listing')
        if request.POST["bid"] > listing.price:
            bid = Bid.objects.create(user=user, amount=request.POST["bid"], listing=listing)
            bid.save()
            listing.price = bid.amount 
            listing.save()
    #TODO


@login_required
def placebid(request):
    listing = validate_listing_query(request)
    user = request.user
    if listing.seller == user:
        return HttpResponseNotAllowed('<h1>405 You cannot place a bid on your own listing</h1>')
    if request.POST["bid"] > listing.price:
        bid = Bid.objects.create(user=user, amount=request.POST["bid"], listing=listing)
        bid.save()
        listing.price = bid.amount 
        listing.save()
    else:
        return HttpResponseBadRequest('<h1>400 The bid amount is too low</h1>')


def invalidoperation(request, msg: str):
    return render(request, 'auctions/user/error.html', {
        'msg': msg
    })


def getwinningbid(listing_id) -> object:
    bids = Bid.objects.filter(listing=listing_id)
    if not bids:
        return None
    highest: int = 0
    for bid in bids:
        if bid.amount > highest:
            highest = bid.amount
            winningbid = bid 
    return winningbid


def validate_listing_query(request):
    try:
        list_id = request.GET.get('id')
        if not list_id:
            raise KeyError
        listing = Listing.objects.get(id=list_id)
    except Listing.DoesNotExist:
        return HttpResponseNotFound('<h1>404 Listing not found</h1>')
    except KeyError:
        return HttpResponseBadRequest('<h1>400 Incorrect URL Parameters</h1>')
    
    return listing
