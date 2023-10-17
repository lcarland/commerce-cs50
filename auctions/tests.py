from django.test import TestCase, RequestFactory, Client  
from django.urls import reverse  
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


    def test_valid_login(self):
        resp = self.client.post(reverse('login'), {"username":"user1","password":"1234"})
        self.assertRedirects(resp, reverse('index'))
        self.assertEqual(resp.wsgi_request.user, self.u1)


    def test_createlisting(self):
        self.client.login(username="user1", password="1234")
        resp = self.client.post(reverse('createlisting'), {
            "title": "Test Product 4", "description": "This is a test product",
            "tags": "hightag, lowtag, purpletag",
            "imgurl": "http://example.com/image.jpg", "startbid": "16.99"
        })
        self.assertRedirects(resp, reverse('userlistings'))
    

    def test_tag_str_to_db(self):
        listing = Mock()
        tags = "foo, bar"
        created_tags = listmng.tag_str_to_db(tags, listing, True)
        self.assertListEqual(['Foo','Bar'], created_tags)


    def test_tag_deleted(self):
        """Checking that cleantags() will purge tags in Catergories
        that don't belong to a listing or to one that has sold."""
        # ['Lions','Tigers','Bears','Foo','Bar']
        tag_objs = self.generate_tags()
        self.listing1.tags.add(tag_objs[0])
        self.listing1.tags.add(tag_objs[1])

        self.listing2.tags.add(tag_objs[2])
        self.listing2.sold = True
              
        del_tags = listmng.cleantags(True)
        self.assertListEqual(del_tags, ['Foo','Bar'])




