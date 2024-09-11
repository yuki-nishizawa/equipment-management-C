from .models import Order

def approval_status_context(request):
    # 未承認の申請の数をカウント
    pending_orders_count = Order.objects.filter(approval_status='承認待ち').count()
    return {'pending_orders_count': pending_orders_count}