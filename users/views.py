from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import ListView,TemplateView,UpdateView #基本機能のビューをインポート
from .forms import CustomUserCreationForm,CustomUserChangeForm      #forms.pyから輸入
from .models import CustomUser #このビュー内でmodels.pyに定義しているCustomUserモデルを使用する
from django.contrib.auth.mixins import LoginRequiredMixin #ログインしていないと見れないようにするためのヤツ
from django.http import HttpResponseForbidden#アクセスを禁止するためのヤツ


class IndexView(TemplateView):
    template_name = 'users/index.html' #テンプレートはusers/index.htmlにする

class SignUpView(generic.CreateView): #新規登録用
    form_class = CustomUserCreationForm #forms.pyで定義しているフォームを使用する
    success_url = reverse_lazy('equipment:list')  # 登録完了後に、備品一覧(equipment/list.html)にリダイレクトする
    template_name = 'users/sign_up.html' #テンプレートはusers/sign_up.htmlにする

class CustomUserListView(LoginRequiredMixin,ListView): #ユーザー一覧用
    #ユーザーの一覧をみるためのビューの名前をCustomUserListViewにする
    #ビューは、ListViewにする
    #LoginRequiredMixinで、ログインしていないと見れないようにする！
    template_name = 'users/users.html' #テンプレートはusers.htmlにする
    model = CustomUser #使用するモデルはCustomUser(→名前はmodels.pyで定義している)
    context_object_name = 'users' #テンプレートにデータを渡すときの名前をusersとする

    def get_queryset(self):
        return CustomUser.objects.order_by('-registration_date') #データを取得する。そのときに、登録日(registration_date)で並び替える。
    
    #管理者以外にユーザー一覧へのアクセスを許可しない
    def dispatch(self, request, *args, **kwargs):#管理者以外にユーザー一覧へのアクセスを許可しない
    # ログインユーザーのis_adminがTrueかどうかをチェック
        if not request.user.is_admin:
            return HttpResponseForbidden("このページにアクセスする権限がありません。")
        return super().dispatch(request, *args, **kwargs)
    


class UserUpdateView(LoginRequiredMixin, UpdateView):
    #ユーザー情報を編集(アップデート）するビューの名前をUserUpdateViewとする
    #ビューは、UpdateViewにする
    #LoginRequiredMixinで、ログインしていないと見れないようにする！
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/edit.html' #テンプレートはedit.htmlにする
    success_url = reverse_lazy('users:users') #編集が成功したら、ユーザー一覧ページに戻る

    def get_object(self, queryset=None):
        # URL から渡された pk を使って、特定のユーザーを取得
        user_id = self.kwargs.get("pk")
        return get_object_or_404(CustomUser, pk=user_id)
