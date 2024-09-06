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
  approval_status = models.CharField(max_length=50, default='承認待ち')
  approval_date = models.DateTimeField(null=True, blank=True)
  approval_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approved_orders', null=True, blank=True)

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