from cart.models import Cart, CartItem
from checkout import serializers
from products.serializers import DiscountSerializer


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    discounts = DiscountSerializer(many=True)

    subtotal = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    discount_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'discounts', 'user_age', 'subtotal', 'discount_total', 'total']

    def get_subtotal(self, obj):
        return obj.calculate_subtotal()

    def get_discount_total(self, obj):
        return obj.calculate_discount_total()

    def get_total(self, obj):
        return obj.calculate_total()
