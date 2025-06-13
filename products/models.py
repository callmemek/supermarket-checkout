from django.db import models
from django.forms import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_weighted = models.BooleanField(default=False)
    age_restricted = models.PositiveIntegerField(null=True, blank=True)  # e.g., 21+

class Discount(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active_from = models.DateTimeField()
    active_to = models.DateTimeField()
    applies_to = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)

    def clean(self):
        if self.discount_type == 'percentage' and self.value >= 100:
            raise ValidationError("Discount cannot be 100% or more.")
        if self.value <= 0:
            raise ValidationError("Discount value must be positive.")
        if self.active_to <= self.active_from:
            raise ValidationError("End date must come after start.")