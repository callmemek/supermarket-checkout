from django.test import TestCase
from decimal import Decimal
from ..models import Product, CartItem, Cart


class AgeVerificationTests(TestCase):

    def setUp(self):
        self.beer = Product.objects.create(name='Beer', product_id='B1', price=Decimal('3.00'), age_restricted=21)

    def test_minor_cannot_purchase_age_restricted_items(self):
        beer_item = CartItem.objects.create(product=self.beer, quantity=1)
        cart = Cart.objects.create(user_age=17)
        cart.items.set([beer_item])
        with self.assertRaises(Exception):
            cart.validate_age_restricted_items()

    def test_adult_can_purchase_age_restricted_items(self):
        beer_item = CartItem.objects.create(product=self.beer, quantity=1)
        cart = Cart.objects.create(user_age=21)
        cart.items.set([beer_item])
        try:
            cart.validate_age_restricted_items()  # should pass
        except:
            self.fail("Age verification failed for valid user")
