from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
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
        
        # GETパラメータからフィルタリングのステータスを取得
        #status_filter = self.request.GET.get('status_filter')
        
        # フィルタリングが選択されている場合は、クエリセットをフィルタリング：ページ送り機能を付ける際に使用
        #if status_filter:
        #    queryset = queryset.filter(approval_status=status_filter)
        
        return queryset