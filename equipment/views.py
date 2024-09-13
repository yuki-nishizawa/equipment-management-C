from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import Equipment,StockChange,Comment
from django.contrib.auth.mixins import LoginRequiredMixin #ログインしてないと見れないようにするやつ
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView
from .forms import EquipForm,StockUpdateForm,CommentForm
from order.forms import OrderForm
from order.models import Order
from django.http import HttpResponseForbidden,HttpResponseRedirect #アクセスを禁止するためのヤツ
from django.http import JsonResponse
from users.models import FavoriteEquip

#備品管理一覧
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


#備品追加ページ
class EquipCreateView(LoginRequiredMixin, CreateView):#CREATE用のビューを使う＆ログインしてないと見れないようにする
    template_name = 'equipment/add.html'# テンプレートはadd.htmlを使用
    model = Equipment # モデル(データベース)は、models.pyで定義しているEquipmentモデルを使用する
    form_class = EquipForm  # フォームは、forms.pyで定義しているEquipFormを使用する
    success_url = reverse_lazy('equipment:list')#登録できたら備品一覧画面に戻る

    def form_valid(self, form):#フォームに入力された内容が形式上正しいかをチェックする
        form.instance.user = self.request.user#チェックできたら登録したユーザーが誰かという情報を取得する、
        return super().form_valid(form)#登録を完了させる

#備品詳細表示ページ
class EquipDetailView(LoginRequiredMixin, DetailView):
    model = Equipment
    template_name = 'equipment/detail.html'
    context_object_name = 'equip' #ここの名前でテンプレート上で呼び出す

    def get_context_data(self, **kwargs):#画像がエラーになった時用の回避策
        context = super().get_context_data(**kwargs)
        equip = context['equip']
        user = self.request.user
        #context['image_url'] = equip.image.url if equip.image else '/static/images/no_image.jpg'# 画像URLが空の場合、デフォルト画像URLを設定：別方法で実装したため不要！一応残しておく
        context['stock_update_form'] = StockUpdateForm(instance=equip) #在庫数更新のフォームが使えるようになる、instance=equipは、今ビューで処理しているequipのデータを初期設定として入れておく、の意味
        context['stock_changes'] = StockChange.objects.filter(equip=equip).order_by('-changed_date')[:5]#StockChangeモデルのデータが使えるようになる
        context['order_form'] = OrderForm() #発注数更新フォームが使えるようになる
        context['orders'] = Order.objects.filter(equip=equip).order_by('-order_date')[:5]#Orderモデルのデータが使えるようになる
        context['is_favorite'] = FavoriteEquip.objects.filter(user=user, equip=equip).exists()# お気に入り情報を追加
        context['favorite_count'] = FavoriteEquip.objects.filter(equip=equip).count()#お気に入り登録人数をカウント
        context['comments'] = Comment.objects.filter(equip=equip).order_by('created_at')
        context['comment_form'] = CommentForm() #コメントフォームが使えるようになる
        return context

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

    #### 発注フォームの処理
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.equip = self.object
            order.user = request.user
            order.save()
            return redirect(self.get_success_url())

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

            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(
            stock_update_form=stock_update_form,
            order_form=order_form
        ))
    def get_success_url(self):
        return reverse_lazy('equipment:detail', kwargs={'pk': self.object.pk})


#備品編集ページ
class EquipUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipForm
    template_name = 'equipment/edit.html'
    
    def get_success_url(self):
        return reverse_lazy('equipment:detail', kwargs={'pk': self.object.pk})
    #管理者以外に備品編集ページへのアクセスを許可しない
    def dispatch(self, request, *args, **kwargs):#管理者以外に備品編集ページへのアクセスを許可しない
    # ログインユーザーのis_adminがTrueかどうかをチェック
        if not request.user.is_admin:
            return HttpResponseForbidden("編集権限がありません。")
        return super().dispatch(request, *args, **kwargs)


#備品削除
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