from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from equipment.models import Equipment
from django.conf import settings

# カスタム ユーザーマネージャー
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


# カスタム ユーザーモデル
class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(unique=True, max_length=50, null=False)
    email = models.EmailField(unique=True, null=False)

    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    

    objects = CustomUserManager()


    def __str__(self):
        return self.email


#お気に入り機能
class FavoriteEquip(models.Model):
    class Meta:
        unique_together = ('user', 'equip')
        db_table = 'favorite'  # ここでテーブル名を指定

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    equip = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.equip.name}"