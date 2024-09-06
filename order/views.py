from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone  # 追加
from .models import Order

# 発注履歴表示機能
class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'order/history.html'
    model = Order
    context_object_name = 'orders'
    #paginate_by = 5  # 1ページに表示する発注数：ページ送り機能を付ける際に使用

    def get_queryset(self):
        # すべての注文を取得し、発注日の降順に並べ替える
        queryset = Order.objects.order_by('-order_date')
        return queryset
    
    def post(self, request, *args, **kwargs):
        # 承認ボタンが押された場合の処理
        if 'approve_order' in request.POST:
            order_id = request.POST.get('approve_order')
            order = get_object_or_404(Order, pk=order_id)
            if request.user.is_admin:
                order.approval_status = '承認済み'
                order.approval_user = request.user
                order.approval_date = timezone.now()  # 現在の日時をセット
                order.save()
                messages.success(request, '発注が承認されました。')
            else:
                messages.error(request, '管理者のみ承認できます。')
        # 否決ボタンが押された場合の処理
        elif 'reject_order' in request.POST:
            order_id = request.POST.get('reject_order')
            order = get_object_or_404(Order, pk=order_id)
            if request.user.is_admin:
                order.approval_status = '否決'
                order.approval_user = request.user
                order.approval_date = timezone.now()  # 否決時にも現在の日時をセット
                order.save()
                messages.success(request, '発注が否決されました。')
            else:
                messages.error(request, '管理者のみ否決できます。')
        return redirect('order:history')  # 発注履歴ページにリダイレクト
