from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, DiscountViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'discounts', DiscountViewSet)


urlpatterns = [
    path('', include(router.urls)),
]