from django.urls import path

from auctions.views import index, listmng

urlpatterns = [
    path("", index.index, name="index"),
    path("login", index.login_view, name="login"),
    path("logout", index.logout_view, name="logout"),
    path("register", index.register, name="register"),
    
    path("createlisting", listmng.createlisting, name="createlisting")
]
