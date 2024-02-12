from .models import Order

def order_count(request):
    order_count = 0
    if request.user.is_authenticated:
        try:
            order = Order.objects.filter(user=request.user, is_completed=False).latest('id')
            order_count = order.orderitem_set.count()
        except Order.DoesNotExist:
            pass

    return {'order_count': order_count}