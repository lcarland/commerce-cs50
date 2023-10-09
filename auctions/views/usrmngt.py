from django.shortcuts import render 


def createlisting(request):
    if request.method == 'POST':
        pass
        #TODO 

    return render(request, 'auctions/createlisting.html', {
        'message' : ''
    })