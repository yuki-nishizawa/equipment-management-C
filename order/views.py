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
    # paginate_by = 5  # 1ページに表示する発注数：ページ送り機能を付ける際に使用
    def get_queryset(self):
        # すべての注文を取得し、発注日の降順に並べ替える
        queryset = Order.objects.order_by('-order_date')
        return queryset
    
    def post(self, request, *args, **kwargs):
        # 承認ボタンまたは否決ボタンが押された場合の処理
        if 'approve_order' in request.POST or 'reject_order' in request.POST:
            order_id = request.POST.get('approve_order') or request.POST.get('reject_order')
            order = get_object_or_404(Order, pk=order_id)
            
            if request.user.is_admin:
                if 'approve_order' in request.POST:
                    order.approval_status = '承認済み'
                    messages.success(request, '発注が承認されました。')
                elif 'reject_order' in request.POST:
                    order.approval_status = '否決'
                    messages.success(request, '発注が否決されました。')
                
                # コメントを取得して保存
                comment = request.POST.get('comment', '－')  # コメントがない場合は「－」をセット
                order.approval_comment = comment
                order.approval_user = request.user
                order.approval_date = timezone.now()  # 現在の日時を保存
                order.save()
            else:
                messages.error(request, '管理者のみ操作可能です。')
        
        return redirect('order:history')  # 発注履歴ページにリダイレクト
