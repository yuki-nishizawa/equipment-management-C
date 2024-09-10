from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm #フォームの基本の形をインポート
from django.contrib.auth import get_user_model #ユーザー情報の基本の形をインポート

class CustomUserCreationForm(UserCreationForm):#ユーザーを新規登録するときに使うフォーム
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # カスタムユーザーモデルを取得
        fields = ('email', 'username','is_staff','is_admin') #フォームを呼び出したときに表示されてほしい項目(modelsで定義している名前を指定)
        labels = {  #フォームを表示したときに、ラベルとして表示されてほしい文字列
         'username':'ユーザー名',
         'email': 'メールアドレス',
         'is_staff': 'スタッフとして登録する',
         'is_admin': '管理者として登録する',
      }
        
class CustomUserChangeForm(UserChangeForm): #ユーザーの情報を変更するときに使うフォーム
    class Meta:
        model = get_user_model() # カスタムユーザーモデルを取得
        fields = ('email', 'username', 'is_staff', 'is_admin')
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
            'is_staff': 'スタッフとして登録する',
            'is_admin': '管理者として登録する',
        }

    def clean_username(self): #変更するときに、ユーザーネームがエラーかどうかをチェックする
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('このユーザー名は既に使用されています。') # もし既に存在する場合は、ValidationErrorを発生させる
        return username # エラーがなければ、ユーザー名を返す

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('このメールアドレスは既に使用されています。')
        return email
        
