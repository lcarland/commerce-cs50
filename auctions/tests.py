from django.test import TestCase, RequestFactory, Client  
from django.urls import reverse  
from django.db.models import Q
from unittest.mock import patch, Mock

from auctions.views import listmng
from .models import Listing, User, Category


# Create your tests here.
class ModelTest(TestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user("user1", "user1@email.com", "1234")
        self.u2 = User.objects.create_user("user2", "user2@email.com", "123456")

        # Category.objects.create(keyword="tag1")
        # Category.objects.create(keyword="tag2")
        # Category.objects.create(keyword="tag3")

        self.listing1 = Listing.objects.create(
            title="Product number 1",
            seller=self.u1,
            description="enter description here",
            imgurl="https://www.image.com",
            startbid=14.00,
            price=14.00
        )
        self.listing2 = Listing.objects.create(
            title="Product number 2",
            seller=self.u2,
            description="enter description here",
            imgurl="https://www.image2.com",
            startbid=14.00,
            price=14.00
        )
        self.listing3 = Listing.objects.create(
            title="Product number 3",
            seller=self.u1,
            description="Some description enetered here.",
            startbid=50.00,
            price=50.00
        )
        self.factory = RequestFactory()
        self.client = Client()

    
    def generate_tags(self, tag_set:list=None) -> list:
        if not tag_set:
            tag_set = ['Lions','Tigers','Bears','Foo','Bar']
        tag_objs = []
        for _tag in tag_set:
            ntag = Category.objects.create(keyword=_tag)
            tag_objs.append(ntag)
        return tag_objs


    def test_default_img(self):
        """Make sure default image is loaded into Listing entry"""
        listing = Listing.objects.get(title="Product number 3")
        self.assertEqual(listing.imgurl, "/static/auctions/product-placeholder.jpg")


    def test_register_new_user(self):
        resp = self.client.post(reverse('register'), {
            "username": "new_user", "email": "someEmail@web.com",
            "password": "1234", "confirmation": "1234",
        })
        self.assertRedirects(resp, reverse('index'))
        user = resp.wsgi_request.user
        self.assertTrue(user.is_authenticated)

    
    def test_register_taken_username(self):
        """username is already taken"""
        resp = self.client.post(reverse('register'), {
            "username": "user1", "email": "user4@email.com",
            "password": "1234", "confirmation": "1234"
        })
        self.assertTemplateUsed(resp, "auctions/register.html")


    def test_login(self):
        resp = self.client.post(reverse('login'), {"username":"user1","password":"1234"})
        self.assertRedirects(resp, reverse('index'))
        self.assertEqual(resp.wsgi_request.user, self.u1)

        resp = self.client.post(reverse('login'), {"username":"user1","password":"123"})
        self.assertTemplateUsed(resp, "auctions/login.html")


    def test_logout(self):
        self.client.login(username="user1", password="1234")
        resp = self.client.get(reverse('logout'))
        self.assertNotEqual(resp.wsgi_request.user, self.u1)


    def test_view_listing(self):
        resp = self.client.get(f"{reverse('viewlisting')}?id=1")
        self.assertTemplateUsed(resp, "auctions/viewlisting.html")

        resp = self.client.get(f"{reverse('viewlisting')}?id=100")
        self.assertEqual(404, resp.status_code)


    def test_createlisting(self):
        self.client.login(username="user1", password="1234")
        resp = self.client.post(reverse('createlisting'), {
            "title": "Test Product 4", "description": "This is a test product",
            "tags": "hightag, lowtag, purpletag",
            "imgurl": "http://example.com/image.jpg", "startbid": "16.99"
        })
        self.assertRedirects(resp, reverse('userlistings'))
        listing4 = Listing.objects.get(title="Test Product 4")
        tags = Category.objects.filter(listing=listing4)
        self.assertEqual(3, len(tags))

        resp = self.client.post(reverse('createlisting'), {
            "title": "Test5", "description": "This is a test product",
            "tags": "hightag, lowtag, purpletag",
            "imgurl": "", "startbid": "16.99"
        })
        with_missing_url = Listing.objects.get(title="Test5")
        imgurl = with_missing_url.imgurl
        self.assertEqual("/static/auctions/product-placeholder.jpg", imgurl)
    

    def test_tag_str_to_db(self):
        listing = Mock()
        tags = "foo, bar,, help,"
        listmng.tag_str_to_db(tags, listing)
        tag_query = Category.objects.filter(
            Q(keyword="Foo") | Q(keyword="Bar") | Q(keyword="Help")
        )
        self.assertEqual(3, len(tag_query))


    def test_tag_deleted(self):
        """Checking that cleantags() will purge tags in Catergories
        that don't belong to a listing or to one that has sold."""
        # ['Lions','Tigers','Bears','Foo','Bar']
        def tag_query():
            return Category.objects.filter(
                Q(listing__isnull=True) | Q(listing__sold=True)
            )
        tag_objs = self.generate_tags()
        self.listing1.tags.add(tag_objs[0])
        self.listing1.tags.add(tag_objs[1])

        self.listing2.tags.add(tag_objs[2])
        self.listing2.sold = True
        
        self.assertEqual(2, len(tag_query()))
        listmng.cleantags()
        self.assertEqual(0, len(tag_query()))

    
    def test_validate_listing_query(self):
        request = Mock()
        request.user = self.u2 
        
        request.POST = {"id":"2"}
        listing = listmng.validate_listing_query(request)
        self.assertEqual(listing, self.listing2)

        request.POST = {"id": "3"}
        self.assertNotEqual(self.listing3, listmng.validate_listing_query(request))




