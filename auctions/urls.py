from django.urls import path

from auctions.views import index, listmng, usermng

urlpatterns = [
    path("", index.index, name="index"),
    path("login", index.login_view, name="login"),
    path("logout", index.logout_view, name="logout"),
    path("register", index.register, name="register"),
    
    path("createlisting", listmng.createlisting, name="createlisting"),
    path("user/listing", listmng.listing_operation, name="listing_operations"),

    path("user", usermng.viewuser, name="viewuser"),
    path("user/viewlistings", usermng.userlistings, name="userlistings"),
    path("user/bids", usermng.userbids, name="userbids"),
    path("user/comments", usermng.usercomments, name="usercomments")
]
