from .models import Cart, CartItem
from .views import _cart_id

# Use context_processors when you need a context in every page, e.g. when you need to pass context to your navbar.

# This function counts how many items are in the cart so you can display it in the navbar on any page.
def counter(request):
    item_count = 0

    if 'admin' in request.path:
        return {}

    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:
                item_count += cart_item.quantity

        except Cart.DoesNotExist:
            item_count = 0

        return dict(item_count = item_count)
