from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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