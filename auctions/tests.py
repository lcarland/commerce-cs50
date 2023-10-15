from django.test import TestCase

from .models import Listing, User, Category

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self) -> None:
        u1 = User.objects.create_user("user1", "user1@email.com", "1234")
        u2 = User.objects.create_user("user2", "user2@email.com", "123456")

        Category.objects.create(keyword="tag1")
        Category.objects.create(keyword="tag2")
        Category.objects.create(keyword="tag3")

        Listing.objects.create(
            title="Product number 1",
            seller=u1,
            description="enter description here",
            imgurl="https://www.image.com",
            startbid=14.00,
            price=14.00
        )
        Listing.objects.create(
            title="Product number 2",
            seller=u2,
            description="enter description here",
            imgurl="https://www.image2.com",
            startbid=14.00,
            price=14.00
        )
        Listing.objects.create(
            title="Product number 3",
            seller=u1,
            description="Some description enetered here.",
            startbid=50.00,
            price=50.00
        )

    def test1(self):
        listing = Listing.objects.get(title="Product number 3")
        self.assertEqual(listing.imgurl, "/static/auctions/product-placeholder.jpg")

    def test2(self):
        listing = Listing.objects.get(title="Product number 1")
        self.assertEqual(listing.startbid, 14.00)
    
    def test3(self):
        listing = Listing.objects.get(id=1)
        user = User.objects.get(id=1)
        self.assertEqual(listing.seller, user)