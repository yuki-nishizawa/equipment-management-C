from django.urls import path
from .views import equipment_list

urlpatterns = [
    path('', equipment_list, name='equipment_list'),
]