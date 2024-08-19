from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('equipment/', include('equipment.urls')),#equipmentのurls.pyへ接続
    path('', include('users.urls')),              #usersアプリのurls.pyへ接続
    path('logout/', LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#画像ファイルをどこに格納するか→場所はsettings.pyで指定