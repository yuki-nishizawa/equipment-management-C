from django.db import models
from django.conf import settings
from equipment.models import Equipment
from django.utils import timezone

class Order(models.Model):
  class Meta:
    db_table = 'order'#テーブルの名前をorderにする

  equip = models.ForeignKey(Equipment, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
  quantity = models.PositiveIntegerField()
  order_date = models.DateTimeField(auto_now_add=True)
  loan_date = models.DateField(null=True, blank=True)  # 貸出希望日を追加
  return_date = models.DateField(null=True, blank=True)  # 返却予定日を追加
  approval_status = models.CharField(max_length=50, default='承認待ち')
  approval_date = models.DateTimeField(null=True, blank=True)
  approval_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approved_orders', null=True, blank=True)
  approval_comment = models.TextField(null=True, blank=True)  # コメント用フィールドを追加 # コメントがない場合もあるため、null=True, blank=Trueに設定

  def approve(self, approver):
      """承認処理"""
      self.approval_status = '承認済み'
      self.approval_date = timezone.now()
      self.approval_user = approver
      self.save()
  def reject(self, approver):
      """否決処理"""
      self.approval_status = '否決'
      self.approval_date = timezone.now()
      self.approval_user = approver
      self.save()   