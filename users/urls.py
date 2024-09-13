from django.urls import path
from .views import IndexView, SignUpView, CustomUserListView, UserUpdateView, MenuView, MyPageView,ForgetPasswordView,FavoriteListView
from django.contrib.auth.views import LoginView,LogoutView

app_name = "users"
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('users/', CustomUserListView.as_view(), name='users'),#ユーザー一覧
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='edit'),#ユーザーを編集
    path('register/', SignUpView.as_view(), name='register'),#新規登録
    path('login/', LoginView.as_view(template_name='users/sign_in.html'), name='login'),#ログイン機能
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),#ログアウト機能
    path('menu/', MenuView.as_view(), name='menu'),#ログアウト機能
    path('mypage/', MyPageView.as_view(), name='mypage'),  # マイページへのパス
    path('forgetpw/', ForgetPasswordView.as_view(), name='forgetpw'),  # マイページへのパス
    path('favorite/', FavoriteListView.as_view(), name='favorite'),  # お気に入り一覧へのパス
]

