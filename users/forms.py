from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # カスタムユーザーモデルを取得
        fields = ('email', 'username','is_staff','is_admin') 
        labels = {
         'username':'ユーザー名',
         'email': 'email',
         'is_staff': 'スタッフとして登録する',
         'is_admin': '管理者として登録する',
      }