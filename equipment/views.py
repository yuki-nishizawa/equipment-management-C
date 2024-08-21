from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import Equipment,StockChange
from django.contrib.auth.mixins import LoginRequiredMixin #ログインしてないと見れないようにするやつ
from django.views.generic import CreateView,DetailView
from .forms import EquipForm,StockUpdateForm
from order.forms import OrderForm
from order.models import Order

#備品管理一覧
def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'equipment/list.html', {'equipments': equipments})#equipment_list.htmlをlist.htmlに修正



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
        #context['image_url'] = equip.image.url if equip.image else '/static/images/no_image.jpg'# 画像URLが空の場合、デフォルト画像URLを設定：別方法で実装したため不要！一応残しておく
        context['stock_update_form'] = StockUpdateForm(instance=equip) #在庫数更新のフォームが使えるようになる
        context['stock_changes'] = StockChange.objects.filter(equip=equip).order_by('-changed_date')[:5]
        context['order_form'] = OrderForm() #発注数更新
        context['orders'] = Order.objects.filter(equip=equip).order_by('-order_date')[:5]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        previous_stock = self.object.stock# フォームを保存する前に、更新前の在庫数を取得しておく

    # 在庫数更新フォームの処理
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

            return redirect(self.get_success_url())

        # 発注フォームの処理
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.equip = self.object
            order.user = request.user
            order.save()
            return redirect(self.get_success_url())

        # 発注承認処理
        order_id = request.POST.get('approve_order')
        if order_id:
            order = get_object_or_404(Order, pk=order_id)
            order.approve(request.user)


        return self.render_to_response(self.get_context_data(
            stock_update_form=stock_update_form,
            order_form=order_form
        ))

    def get_success_url(self):
        return reverse_lazy('equipment:detail', kwargs={'pk': self.object.pk})