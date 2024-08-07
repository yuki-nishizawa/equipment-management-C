from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('equipment/', include('equipment.urls')),#equipmentのurls.pyへ接続
    path('', include('users.urls')),              #usersアプリのurls.pyへ接続
    path('logout/', LogoutView.as_view(), name='logout'),
]
