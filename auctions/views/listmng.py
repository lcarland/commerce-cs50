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

        tags = tags.split(',')

        try:
            listing = Listing.objects.create(title=title, description=description, imgurl=imgurl, startbid=startbid)
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