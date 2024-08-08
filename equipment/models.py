from django.db import models

#備品情報のモデルを定義
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
