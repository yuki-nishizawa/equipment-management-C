from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm      #forms.pyから輸入

class IndexView(TemplateView):
    template_name = 'users/index.html'

class SignUpView(generic.CreateView): #新規登録用
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:index')  # 一旦仮置き。登録完了後に、備品一覧(equipment/list.html)リダイレクトするようにする。
    template_name = 'users/sign_up.html'
