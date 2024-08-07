from django.urls import path
from .views import IndexView,SignUpView
from django.contrib.auth.views import LoginView,LogoutView

app_name = "users"
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', SignUpView.as_view(), name='register'),#新規登録
    path('login/', LoginView.as_view(template_name='users/sign_in.html'), name='login'),#ログイン機能
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),#ログアウト機能
]

