# products/tests/test_product_validation.py
import pytest
from products.models import Product
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_invalid_product_id_xss():
    product = Product(name="Bad", product_id="<script>alert(1)</script>", price=5.00)
    with pytest.raises(ValidationError):
        product.full_clean()
