from django.db import models
from django.conf import settings

#備品管理に関係するデータベースを定義
class Equipment(models.Model):
  class Meta:
    db_table = 'equip'
    #テーブルの名前を'equip'にする
    #(ここで定義しない場合は、アプリケーション名 と モデル名 をアンダースコアでつないだものがテーブル名になる： 'equipment_equipment')

  equip_name = models.CharField(max_length=50,null=False)
  category = models.CharField(max_length=50,null=False)
  place = models.CharField(max_length=50,null=False)
  condition  = models.CharField(max_length=50,null=False)
  stock = models.PositiveIntegerField(null=False)
  text = models.TextField(null=False)
  image = models.ImageField(upload_to='images/', blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)


#在庫数変更履歴に関係するデータベースを定義
class StockChange(models.Model):
    class Meta:
      db_table = 'stockchange'
       #テーブルの名前を'stockchange'にする

    equip = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    changed_date = models.DateTimeField(auto_now_add=True)
    previous_stock = models.PositiveIntegerField()
    new_stock = models.PositiveIntegerField()