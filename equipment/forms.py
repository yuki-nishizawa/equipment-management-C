from .models import Equipment,Comment
from django import forms

class EquipForm(forms.ModelForm):
    class Meta:
      model = Equipment
      fields = ['equip_name','category', 'condition','loan_status','place','text','image','stock']
      labels = {
         'equip_name':'名前',
         'category': 'カテゴリ',
         'condition': '状態',
         'loan_status': '貸出状況',
         'place': '設置場所',
         'text': '説明',
         'image': '画像',
         'stock': '在庫数',
      }

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['stock']
        labels = {
         'stock': '在庫数',
      }

class CommentForm(forms.ModelForm):
    class Meta:
      model = Comment
      fields = ['text']
      labels = {
         'text': 'コメント',
      }
      widgets = {
         'text': forms.Textarea(attrs={'placeholder': 'コメントを入力...'}),
        }