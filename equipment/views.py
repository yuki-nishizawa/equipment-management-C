from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Equipment
from django.contrib.auth.mixins import LoginRequiredMixin #ログインしてないと見れないようにするやつ
from django.views.generic import CreateView
from .forms import EquipForm

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