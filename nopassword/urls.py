# -*- coding: utf8 -*-
from django.urls import path

from nopassword import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/code/', views.LoginCodeView.as_view(), name='login_code'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
