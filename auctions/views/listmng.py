from django.shortcuts import render 
from django.db import IntegrityError

from ..models import Listing


def createlisting(request):
    message: str = ""

    #TODO authentication

    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        tags = request.POST["tags"] # type str -> list
        imgurl = request.POST["imgurl"]
        startbid: float = request.POST["startbid"]

        tags = tags.split(',')

        for i, val in enumerate(tags):
            tags[i] = val.strip()
            if not val:
                del tags[i]
            
        try:
            listing = Listing.objects.create(title=title, description=description, tags=tags, imgurl=imgurl, startbid=startbid)
            listing.save()
        except IntegrityError:
            render(request, 'auctions/createlisting.html', {
                'message': "Error submitting listing"
            })
        
        message = "Listing posted"


    return render(request, 'auctions/createlisting.html', {
        'message' : message
    })