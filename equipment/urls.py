from django.urls import path
from .views import equipment_list,EquipCreateView

app_name = 'equipment'#逆引きするときにどういう名前で呼び出すか…たとえば、equipment:list等の名前で呼び出せるようになる app_name:name(urlpatternsの中のname)

urlpatterns = [
    path('', equipment_list, name='list'),#equipment/(空のパス)/にアクセスが来たら、views.pyで定義しているequipment_listを参照する
    path('add/', EquipCreateView.as_view(), name='add'),##equipment/add/にアクセスが来たら、views.pyで定義しているEquipCreateViewを参照する
]