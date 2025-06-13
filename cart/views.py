# cart/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal
from .models import Cart, CartItem
from products.models import Product

@require_POST
def add_item_to_cart(request, cart_id):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    cart = Cart.objects.get(id=cart_id)

    try:
        product = Product.objects.get(product_id=product_id)
        quantity = Decimal(quantity)
        if quantity <= 0:
            return JsonResponse({'error': 'Quantity must be positive'}, status=400)
    except:
        return JsonResponse({'error': 'Invalid product or quantity'}, status=400)

    existing_item = cart.items.filter(product=product).first()
    if existing_item:
        existing_item.quantity += quantity
        existing_item.save()
    else:
        item = CartItem.objects.create(product=product, quantity=quantity)
        cart.items.add(item)

    return JsonResponse({'message': 'Item added'})
