from django.shortcuts import render 
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from ..models import Listing, Category


@login_required
def createlisting(request):
    message: str = ""

    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        tags = request.POST["tags"] # type str -> list
        imgurl = request.POST["imgurl"]
        startbid: float = request.POST["startbid"]
        seller_id = request.user.id

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

    if operation == 'accept':
        listing = Listing.objects.get(id=list_id)
        if not listing:
            return invalidoperation(request, 'Ivalid Listing Provided')
        if listing.seller != user.id:
            return invalidoperation(request, 'This Listing does not belong to you!')
        listing.sold = True 
    elif operation == 'close':
        pass 
    elif operation == 'edit':
        pass 
    else:
        pass


def invalidoperation(request, msg: str):
    return render(request, 'auctions/user/error.html', {
        'msg': msg
    })