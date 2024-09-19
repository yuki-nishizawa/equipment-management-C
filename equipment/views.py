from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import Equipment,StockChange,Comment
from django.contrib.auth.mixins import LoginRequiredMixin #ログインしてないと見れないようにするやつ
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView,TemplateView
from .forms import EquipForm,StockUpdateForm,CommentForm
from order.forms import OrderForm
from order.models import Order
from django.http import HttpResponseForbidden,HttpResponseRedirect,HttpResponse,JsonResponse #アクセスを禁止するためのヤツ
from users.models import FavoriteEquip
from datetime import datetime, timedelta
import calendar
from django.utils import timezone
from django.template.loader import render_to_string

#書籍管理一覧
@login_required#ログインしていないと見れないようにするデコレータを追加
def equipment_list(request):
    equipments = Equipment.objects.all().order_by('-updated_at')
    return render(request, 'equipment/list.html', {'equipments': equipments})#equipment_list.htmlをlist.htmlに修正 #テンプレート上で、データをequipmentsという名前で呼び出す

# 貸出処理
def loan_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.loan_status = '貸出中'
    equipment.save()
    return redirect('equipment:list')

# 返却処理
def return_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.loan_status = '貸出可'
    equipment.save()
    return redirect('equipment:list')


#書籍追加ページ
class EquipCreateView(LoginRequiredMixin, CreateView):#CREATE用のビューを使う＆ログインしてないと見れないようにする
    template_name = 'equipment/add.html'# テンプレートはadd.htmlを使用
    model = Equipment # モデル(データベース)は、models.pyで定義しているEquipmentモデルを使用する
    form_class = EquipForm  # フォームは、forms.pyで定義しているEquipFormを使用する
    success_url = reverse_lazy('equipment:list')#登録できたら備品一覧画面に戻る

    def form_valid(self, form):#フォームに入力された内容が形式上正しいかをチェックする
        form.instance.user = self.request.user#チェックできたら登録したユーザーが誰かという情報を取得する、
        return super().form_valid(form)#登録を完了させる

#書籍詳細表示ページ
class EquipDetailView(LoginRequiredMixin, DetailView):
    model = Equipment
    template_name = 'equipment/detail.html'
    context_object_name = 'equip' #ここの名前でテンプレート上で呼び出す

    def get_context_data(self, **kwargs):#画像がエラーになった時用の回避策
        context = super().get_context_data(**kwargs)
        equip = context['equip']
        user = self.request.user
        now = timezone.now().date()  # 現在の日付を取得

        context['stock_update_form'] = StockUpdateForm(instance=equip) #在庫数更新のフォームが使えるようになる、instance=equipは、今ビューで処理しているequipのデータを初期設定として入れておく、の意味
        context['stock_changes'] = StockChange.objects.filter(equip=equip).order_by('-changed_date')[:5]#StockChangeモデルのデータが使えるようになる
        context['order_form'] = OrderForm() #貸出数更新フォームが使えるようになる
        context['orders'] = Order.objects.filter(equip=equip).order_by('-order_date')[:5]#Orderモデルのデータが使えるようになる
        context['is_favorite'] = FavoriteEquip.objects.filter(user=user, equip=equip).exists()# お気に入り情報を追加
        context['favorite_count'] = FavoriteEquip.objects.filter(equip=equip).count()#お気に入り登録人数をカウント
        context['comments'] = Comment.objects.filter(equip=equip).order_by('created_at')
        context['comment_form'] = CommentForm() #コメントフォームが使えるようになる

        # 貸出予定リスト用！承認済みで、貸出希望日または返却予定日が未来のものを取得し、5件に絞る
        context['future_orders'] = (
            Order.objects.filter(
                equip=equip,
                approval_status='承認済み',
                loan_date__gte=now  # 貸出希望日が現在以降
            )
            .union(
                Order.objects.filter(
                    equip=equip,
                    approval_status='承認済み',
                    return_date__gte=now  # 返却予定日が現在以降
                )
            )
            .order_by('loan_date')[:5]  # 貸出希望日でソートして5件に絞る
        )



        # カレンダー部分のコンテキストをヘルパーメソッドで取得
        calendar_context = get_calendar_context(
            request=self.request,
            year=self.request.GET.get('year'),
            month=self.request.GET.get('month'),
            equip=self.object
        )

        # カレンダーのコンテキストをマージする
        context.update(calendar_context)

        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # AJAXリクエストの場合、カレンダーの部分だけ返す
            html = render_to_string('equipment/calendar_partial.html', context, request=self.request)
            return HttpResponse(html)
        else:
            # 通常のリクエストの場合、全体を返す
            return super().render_to_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        previous_stock = self.object.stock# フォームを保存する前に、更新前の在庫数を取得しておく

    ### 在庫数更新フォームの処理
        stock_update_form = StockUpdateForm(request.POST, instance=self.object)
        if stock_update_form.is_valid():
        # フォームを保存する
            updated_equip = stock_update_form.save()

        # StockChangeテーブルに変更履歴を保存
            StockChange.objects.create(
            equip=self.object,
            user=request.user,
            previous_stock=previous_stock,
            new_stock=updated_equip.stock,
        )

    #### 貸出フォームの処理
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.equip = self.object
            order.user = request.user
            order.save()
            return redirect(self.get_success_url() + '?loan_success=true')

        # 承認ボタンが押されたかを確認
        order_id = request.POST.get('approve_order')
        if order_id:
            order = get_object_or_404(Order, pk=order_id)
            order.approve(request.user)  # Orderモデルにある'approve'メソッドを使って承認処理を実行
            return HttpResponseRedirect(request.path_info)  # リダイレクトして、ページ更新時の再送信を防ぐ
 
        # 否決ボタンが押されたかを確認
        reject_order_id = request.POST.get('reject_order')
        if reject_order_id:
            order = get_object_or_404(Order, pk=reject_order_id)
            order.reject(request.user)  # Orderモデルに'reject'メソッドを定義し、否決処理を実行
            return HttpResponseRedirect(request.path_info)  # リダイレクトして、ページ更新時の再送信を防ぐ

    ### お気に入り機能
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # お気に入り登録・解除の処理
            equip_id = request.POST.get('equip_id')
            equipment = get_object_or_404(Equipment, id=equip_id)
            user = request.user

            favorite, created = FavoriteEquip.objects.get_or_create(user=user, equip=equipment)
            if not created:
                favorite.delete()
                favorite_count = FavoriteEquip.objects.filter(equip=equipment).count()
                return JsonResponse({'status': 'removed', 'favorite_count': favorite_count})
            else:
                favorite_count = FavoriteEquip.objects.filter(equip=equipment).count()
                return JsonResponse({'status': 'added', 'favorite_count': favorite_count})

        ### コメント機能
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.equip = self.object
            comment.user = request.user
            comment.save()

            return redirect(self.get_success_url() + '?comment_success=true')

        return self.render_to_response(self.get_context_data(
            stock_update_form=stock_update_form,
            order_form=order_form
        ))
    def get_success_url(self):
        return reverse_lazy('equipment:detail', kwargs={'pk': self.object.pk})


#書籍編集ページ
class EquipUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipForm
    template_name = 'equipment/edit.html'
    
    def get_success_url(self):
         return reverse_lazy('equipment:detail', kwargs={'pk': self.object.pk}) + '?success=true'
    #管理者以外に書籍編集ページへのアクセスを許可しない
    def dispatch(self, request, *args, **kwargs):#管理者以外に書籍編集ページへのアクセスを許可しない
    # ログインユーザーのis_adminがTrueかどうかをチェック
        if not request.user.is_admin:
            return HttpResponseForbidden("編集権限がありません。")
        return super().dispatch(request, *args, **kwargs)


#書籍削除
class EquipDeleteView(LoginRequiredMixin, DeleteView): #アクセスがきたら削除するだけなのでテンプレートの設定はなし
    model = Equipment
    success_url = reverse_lazy('equipment:list')

    def dispatch(self, request, *args, **kwargs):#管理者以外に削除機能へのアクセスを許可しない
    # ログインユーザーのis_adminがTrueかどうかをチェック
        if not request.user.is_admin:
            return HttpResponseForbidden("削除権限がありません。")
        return super().dispatch(request, *args, **kwargs)


#コメント削除機能
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        # コメントが関連付けられている備品の詳細ページにリダイレクトする
        return reverse_lazy('equipment:detail', kwargs={'pk': self.object.equip.pk})

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()

        # コメント投稿者または管理者のみが削除可能
        if request.user != comment.user and not request.user.is_admin:
            return HttpResponseForbidden("このコメントを削除する権限がありません。")
        
        return super().dispatch(request, *args, **kwargs)



#カレンダー機能：ヘルパーメソッド
def get_calendar_context(request, year=None, month=None, equip=None):
    # URLから年と月のパラメータを取得し、明示的にint型に変換
    year = int(request.GET.get('year', datetime.now().year)) if year is None else int(year)
    month = int(request.GET.get('month', datetime.now().month)) if month is None else int(month)

    # 月の最初の日が何曜日か（0=月曜日, 6=日曜日）とその月の日数を取得
    first_weekday, days_in_month = calendar.monthrange(year, month)

    # 月曜日始まりから日曜日始まりに変換
    if first_weekday == 6:  # 日曜日の場合
        first_weekday = 0
    else:
        first_weekday += 1

    days_in_month_range = range(1, days_in_month + 1)

    # 空のセルの数（first_weekday の値分）
    empty_days = range(first_weekday)

    # 貸出予定を取得（フィルタ条件はアプリに応じて変更）
    loaned_days = set()
    future_orders = Order.objects.filter(
        equip=equip,
        loan_date__year=year,
        loan_date__month=month,
        approval_status='承認済み'
    )

    # 貸出日をセットに格納
    for order in future_orders:
        loan_date = order.loan_date
        return_date = order.return_date
        current_day = loan_date
        while current_day <= return_date and current_day.month == month:
            loaned_days.add(current_day.day)
            current_day += timedelta(days=1)

    # 前月と次月の計算
    if month == 1:
        prev_month_year = year - 1
        prev_month = 12
    else:
        prev_month_year = year
        prev_month = month - 1

    if month == 12:
        next_month_year = year + 1
        next_month = 1
    else:
        next_month_year = year
        next_month = month + 1

    # コンテキストを返す
    return {
        'days_in_month': days_in_month_range,
        'loaned_days': loaned_days,
        'current_year': year,
        'current_month': month,
        'empty_days': empty_days,  # 空のセル数を渡す
        'prev_month_year': prev_month_year,
        'prev_month': prev_month,
        'next_month_year': next_month_year,
        'next_month': next_month,
    }