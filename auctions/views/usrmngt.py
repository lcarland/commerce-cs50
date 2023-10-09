from django.shortcuts import render 

import re


def createlisting(request):
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
            
        #TODO

    return render(request, 'auctions/createlisting.html', {
        'message' : ''
    })