from Cart.models import Cart,CartItem
from Cart.views import _get_session_id


def cart_counter(request):
    count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            session_cart=Cart.objects.filter(cart_id=_get_session_id(request))
            cart_items=CartItem.objects.all().filter(cart=session_cart[:1])
            for cart_item in cart_items:
                count+=cart_item.quantity
        except Cart.DoesNotExist:
            count=0
    return dict(cart_count=count)