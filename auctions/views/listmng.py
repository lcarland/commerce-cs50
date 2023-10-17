from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed, Http404
from django.urls import reverse
from django import forms
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from ..models import Listing, Category, Bid, Comment


class ListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    tags = forms.CharField(label="Tags, seperate each tag with a comma.")
    imgurl = forms.URLField(label="Image URL", required=False)
    

class EditListingForm(ListingForm):
    id = forms.HiddenInput()


class CreateListingForm(ListingForm):
    startbid = forms.FloatField(label="Starting Bid")


@require_GET
def viewlisting(request):
    try:
        listing = Listing.objects.get(id=request.GET['id'])
    except:
        raise Http404("Listing not found.")
    tags = Category.objects.filter(listing=listing)
    comments = Comment.objects.filter(listing=listing)

    return render(request, 'auctions/viewlisting.html', {
        'listing': listing,
        'tags': tags,
        'comments': comments
    })


@login_required
@require_http_methods(['GET', 'POST'])
def createlisting(request):
    message: str = ""
    user = request.user

    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        tags = request.POST["tags"] # type str -> list
        imgurl = request.POST["imgurl"]
        startbid: float = request.POST["startbid"]
        seller_id = user

        if not imgurl:
            imgurl = "/static/auctions/product-placeholder.jpg"
        startbid = round(float(startbid), 2)

        try:
            listing = Listing.objects.create(
                title=title, 
                description=description, 
                imgurl=imgurl, 
                seller=seller_id, 
                price=startbid, 
                startbid=startbid
            )
            listing.save()

            user.selling_num += 1
            user.save()
            tag_str_to_db(tags, listing)

        except IntegrityError:
            render(request, 'auctions/createlisting.html', {
                'message': "Error submitting listing",
                "newlisting": True,
                'form': CreateListingForm(initial={
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'imgurl': imgurl,
                    'startbid': startbid
                })
            })
        
        return HttpResponseRedirect(reverse("userlistings"))

    # GET
    return render(request, 'auctions/createlisting.html', {
        'message' : message,
        'newlisting': True,
        'form': CreateListingForm()
    })


@login_required
@require_POST
def listing_operation(request):
    user = request.user
    listing = validate_listing_query(request)
  
    if listing.seller != user:
        return HttpResponseNotAllowed("<h1>405 You are not the owner of this listing</h1>")
    
    operation = request.POST["oper"]

    if operation == 'accept':
        if not listing.winningbid:
            return HttpResponseRedirect(reverse('userlistings'))
        listing.sold = True
        listing.save()
        user.earnings += listing.price 
        user.selling_num -= 1
        user.sold_num += 1
        user.save()
        cleantags()

    elif operation == 'edit':
        tag_objs = Category.objects.filter(listing=listing)
        tags = [obj.keyword for obj in tag_objs]

        return render(request, 'auctions/createlisting.html', {
            'message': '',
            'newlisting': False,
            'form': get_edit_form(listing, tags),
            'id': listing.id
        }) 
    
    elif operation == 'delete':
        listing.delete()
        user.selling_num -= 1
        user.save()
        cleantags()

    else:
        raise ValueError

    return HttpResponseRedirect(reverse("viewuser"))


@login_required
@require_POST
def updatelisting(request):
    listing = validate_listing_query(request)
    user = request.user

    if listing.seller != user:
        return HttpResponseNotAllowed("<h1>405 You are not the owner of this listing</h1>")
    
    listing.title = request.POST["title"]
    listing.description = request.POST["description"]
    listing.imgurl = request.POST["imgurl"]

    if not imgurl:
        imgurl = "/static/auctions/product-placeholder.jpg"

    tags = request.POST["tags"]

    try:
        listing.save()
        tag_str_to_db(tags, listing)
        cleantags()

    except IntegrityError:
        render(request, 'auctions/createlisting.html', {
            'message': "Error submitting listing",
            "newlisting": False,
            'form': get_edit_form(listing, tags),
            'id': listing.id
        })

    return HttpResponseRedirect(reverse("userlistings"))


@login_required
@require_http_methods(['POST'])
def placebid(request):
    listing = Listing.objects.get(id=request.POST["id"])
    user = request.user

    if listing.seller == user:
        return HttpResponseNotAllowed('<h1>405 You cannot place a bid on your own listing</h1>')
    
    if float(request.POST["bid"]) > listing.price:
        bid = Bid.objects.create(user=user, amount=request.POST["bid"], listing=listing)
        bid.save()
        listing.price = bid.amount 
        listing.winningbid = bid
        listing.save()
    else:
        return HttpResponseBadRequest('<h1>400 The bid amount is too low</h1>')
    return HttpResponseRedirect(f"{reverse('viewlisting')}?id={listing.id}")


def tag_str_to_db(tags:str, listing:object):
    tags = tags.split(',')

    for val in tags:
        val = val.strip()
        if not val:
            continue
        val = val.capitalize()
        tag, was_created = Category.objects.get_or_create(keyword=val)
        listing.tags.add(tag)


def cleantags() -> None:
    """Executed on listing update, delete, or accept.
    Purges tags in 'Category' that are no longer used"""
    unused_tags = Category.objects.filter(Q(listing__isnull=True) | Q(listing__sold=True))
    for _tag in unused_tags:
        _tag.delete()


def validate_listing_query(request) -> object: 
    """For validating a user is the owner of a listing"""
    try:
        list_id = request.POST["id"]
        if not list_id:
            raise KeyError
        listing = Listing.objects.get(id=list_id)
    except Listing.DoesNotExist:
        return HttpResponseNotFound('<h1>404 Listing not found</h1>')
    except KeyError:
        return HttpResponseBadRequest('<h1>400 Incorrect URL Parameters</h1>')
    
    if listing.seller != request.user:
        return HttpResponseNotAllowed("<h1>405 You are not the owner of this listing</h1>")
    return listing


def get_edit_form(listing: object, tags: list[str]) -> object:

    return EditListingForm(initial={
        'id': listing.id,
        'title': listing.title,
        'description': listing.description,
        'imgurl': listing.imgurl,
        'tags': ', '.join(map(str, tags))
    })
