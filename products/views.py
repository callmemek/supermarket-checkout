from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer, DiscountSerializer
from .models import Product, Discount
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer