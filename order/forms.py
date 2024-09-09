from .models import Order
from django import forms

#発注フォーム
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'loan_date', 'return_date']  # 貸出希望日と返却予定日を追加
        labels = {
            'quantity': '発注数',
            'loan_date': '貸出希望日',
            'return_date': '返却予定日',
        }
        widgets = {
            'loan_date': forms.DateInput(attrs={'type': 'date'}),  # 貸出希望日の入力形式
            'return_date': forms.DateInput(attrs={'type': 'date'}),  # 返却予定日の入力形式
        }

#発注を承認するためのフォーム
class OrderApprovalForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # フォームのフィールドは空にしておく。POSTリクエストでフォームが提出されたときに、`approve` メソッドを呼び出す。