# cart/tests/test_cart_operations.py
import pytest
from cart.models import Cart, CartItem
from products.models import Product
from decimal import Decimal

@pytest.mark.django_db
def test_add_valid_item_to_cart():
    product = Product.objects.create(name='Apple', product_id='apple1', price=Decimal('1.50'))
    cart = Cart.objects.create(user_age=25)
    item = CartItem.objects.create(product=product, quantity=Decimal('2'))
    cart.items.add(item)
    assert cart.calculate_subtotal() == Decimal('3.00')
