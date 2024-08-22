from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('equipment/', include('equipment.urls')),#equipmentのurls.pyへ接続
    path('', include('users.urls')),              #usersアプリのurls.pyへ接続
    path('order_history/', include('order.urls')),  # orderアプリのurls.pyへ接続
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#画像ファイルをどこに格納するか→場所はsettings.pyで指定