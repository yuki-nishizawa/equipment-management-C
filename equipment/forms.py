from .models import Equipment
from django import forms

class EquipForm(forms.ModelForm):
    class Meta:
      model = Equipment
      fields = ['equip_name','category', 'condition','place','text','image','stock']
      labels = {
         'equip_name':'名前',
         'category': 'カテゴリ',
         'condition': '状態',
         'place': '設置場所',
         'text': '説明',
         'image': '画像',
         'stock': '在庫数',
      }