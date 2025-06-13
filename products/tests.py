from django.test import TestCase
from django.utils import timezone
from .models import Product, Discount
from decimal import Decimal
from datetime import timedelta


class ProductDiscountModelTests(TestCase):

    def setUp(self):
        # Create products
        self.apple = Product.objects.create(name='Apple', product_id='A1', price=Decimal('1.50'))
        self.beer = Product.objects.create(name='Beer', product_id='B1', price=Decimal('3.00'), age_restricted=21)
        self.weighted_cheese = Product.objects.create(name='Cheese', product_id='C1', price=Decimal('2.00'), is_weighted=True)

        # Create active and expired discounts
        now = timezone.now()
        self.active_discount = Discount.objects.create(
            name='10% Off', discount_type='percentage', value=10,
            active_from=now - timedelta(days=1), active_to=now + timedelta(days=1)
        )

        self.expired_discount = Discount.objects.create(
            name='Expired Deal', discount_type='fixed', value=5,
            active_from=now - timedelta(days=10), active_to=now - timedelta(days=1)
        )

    def test_malformed_product_id(self):
        product = Product(name='Eggs', product_id='DROP TABLE', price=Decimal('5.00'))
        try:
            product.full_clean()
        except:
            self.fail("Malformed but safe product_id rejected")
