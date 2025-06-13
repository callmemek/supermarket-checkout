from django.test import TestCase
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from ..models import Cart, CartItem, Discount, Product


class DiscountManagementTests(TestCase):

    def setUp(self):
        # Setup products for use
        self.apple = Product.objects.create(name='Apple', product_id='A1', price=Decimal('1.50'))
        self.weighted_cheese = Product.objects.create(name='Cheese', product_id='C1', price=Decimal('2.00'), is_weighted=True)

    def test_expired_discount_not_applied(self):
        now = timezone.now()
        expired_discount = Discount.objects.create(
            name='Expired Deal', discount_type='fixed', value=5,
            active_from=now - timedelta(days=10), active_to=now - timedelta(days=1)
        )
        item = CartItem.objects.create(product=self.apple, quantity=2)
        cart = Cart.objects.create(user_age=25)
        cart.items.set([item])
        cart.discounts.set([expired_discount])
        self.assertEqual(cart.calculate_discount_total(), 0)

    def test_fixed_discount_on_min_purchase(self):
        discount = Discount.objects.create(
            name='Min Purchase $10', discount_type='fixed', value=3,
            min_purchase=10,
            active_from=timezone.now() - timedelta(days=1),
            active_to=timezone.now() + timedelta(days=1)
        )
        item = CartItem.objects.create(product=self.apple, quantity=5)  # $7.50 < $10
        cart = Cart.objects.create(user_age=25)
        cart.items.set([item])
        cart.discounts.set([discount])
        self.assertEqual(cart.calculate_discount_total(), 0)

    def test_discount_on_specific_item_only(self):
        specific_discount = Discount.objects.create(
            name='Cheese only', discount_type='percentage', value=50,
            applies_to=self.weighted_cheese,
            active_from=timezone.now() - timedelta(days=1),
            active_to=timezone.now() + timedelta(days=1)
        )
        cheese_item = CartItem.objects.create(product=self.weighted_cheese, quantity=1)
        apple_item = CartItem.objects.create(product=self.apple, quantity=1)
        cart = Cart.objects.create(user_age=25)
        cart.items.set([cheese_item, apple_item])
        cart.discounts.set([specific_discount])
        self.assertAlmostEqual(cart.calculate_discount_total(), Decimal('1.00'))  # 50% of $2.00 cheese
