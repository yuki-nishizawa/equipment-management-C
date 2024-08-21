from .models import Order
from django import forms

#発注フォーム
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']
        labels = {
         'quantity': '発注数',
      }

#発注を承認するためのフォーム
class OrderApprovalForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # フォームのフィールドは空にしておく。POSTリクエストでフォームが提出されたときに、`approve` メソッドを呼び出す。