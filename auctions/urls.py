from django.urls import path

from auctions.views import index, listmng, usermng

urlpatterns = [
    path("", index.index, name="index"),
    path("login", index.login_view, name="login"),
    path("logout", index.logout_view, name="logout"),
    path("register", index.register, name="register"),
    
    path("listing", listmng.viewlisting, name="viewlisting"),
    path("placebid", listmng.placebid, name="placebid" ),
    path("createlisting", listmng.createlisting, name="createlisting"),
    path("updatelisting", listmng.updatelisting, name="updatelisting"),
    path("user/listing", listmng.listing_operation, name="listing_operations"),

    path("user", usermng.viewuser, name="viewuser"),
    path("user/viewlistings", usermng.userlistings, name="userlistings"),
    path("user/bids", usermng.userbids, name="userbids"),
    path("user/comments", usermng.usercomments, name="usercomments"),
    path("user/postcomment", usermng.postcomment, name="postcomment"),
    path('user/watchlist', usermng.watchlist, name="watchlist"),
    path("user/remove_from_watchlist", usermng.rmv_from_watch, name="rmv_from_watch")
]
