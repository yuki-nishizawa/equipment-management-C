from django.urls import path
from .views import equipment_list,EquipCreateView,EquipDetailView,EquipUpdateView,EquipDeleteView,CommentDeleteView

app_name = 'equipment'#逆引きするときにどういう名前で呼び出すか…たとえば、equipment:list等の名前で呼び出せるようになる app_name:name(urlpatternsの中のname)

urlpatterns = [
    path('', equipment_list, name='list'),#equipment/(空のパス)/にアクセスが来たら、views.pyで定義しているequipment_listを参照する
    path('add/', EquipCreateView.as_view(), name='add'),#equipment/add/にアクセスが来たら、views.pyで定義しているEquipCreateViewを参照する
    path('<int:pk>', EquipDetailView.as_view(), name='detail'),#equipment/(備品id)/にアクセスが来たら、views.pyで定義しているEquipCreateViewを参照する
    path('<int:pk>/edit/', EquipUpdateView.as_view(), name='edit'),#equipment/(備品id)/edit/にアクセスが来たら、views.pyで定義しているEquipUpdateViewを参照する
    path('<int:pk>/delete/', EquipDeleteView.as_view(), name='delete'),#equipment/(備品id)/delete/にアクセスが来たら、views.pyで定義しているEquipDeleteViewを参照する
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),#コメント削除用機能
]