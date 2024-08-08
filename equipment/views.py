from django.shortcuts import render
from .models import Equipment

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'equipment/list.html', {'equipments': equipments})#equipment_list.htmlをlist.htmlに修正
