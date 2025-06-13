from django.db import models
from products.models import Product, Discount
from decimal import Decimal
from django.utils import timezone

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.product.price * self.quantity

class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    discounts = models.ManyToManyField(Discount, blank=True)
    user_age = models.PositiveIntegerField()

    def calculate_subtotal(self):
        return sum(item.subtotal() for item in self.items.all())

    def calculate_discount_total(self):
        subtotal = self.calculate_subtotal()
        discount_total = Decimal(0)
        for discount in self.discounts.all():
            if not (discount.active_from <= timezone.now() <= discount.active_to):
                continue
            if discount.min_purchase and subtotal < discount.min_purchase:
                continue
            if discount.applies_to:
                for item in self.items.all():
                    if item.product == discount.applies_to:
                        if discount.discount_type == 'percentage':
                            discount_total += item.subtotal() * discount.value / 100
                        else:
                            discount_total += discount.value
            else:
                if discount.discount_type == 'percentage':
                    discount_total += subtotal * discount.value / 100
                else:
                    discount_total += discount.value
        return discount_total

    def calculate_total(self):
        subtotal = self.calculate_subtotal()
        discount_total = self.calculate_discount_total()
        tax = subtotal * Decimal('0.15')
        return max(Decimal(0), subtotal + tax - discount_total)

    def validate_age_restricted_items(self):
        for item in self.items.all():
            if item.product.age_restricted and self.user_age < item.product.age_restricted:
                raise Exception("User is not old enough to purchase this item")

        for discount in self.discounts.all():
            if discount.applies_to and discount.applies_to.age_restricted and self.user_age < discount.applies_to.age_restricted:
                raise Exception("User is not old enough to use this discount")