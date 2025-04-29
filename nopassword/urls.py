# -*- coding: utf8 -*-
from django.urls import path

from nopassword import views

urlpatterns = [
    path(r'^login/$', views.LoginView.as_view(), name='login'),
    path(r'^login/code/$', views.LoginCodeView.as_view(), name='login_code'),
    path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
