# -*- coding: utf-8 -*-
#from django.conf.urls import url
from django.urls import re_path


from nopassword.rest import views

urlpatterns = [
    re_path(r'^login/$', views.LoginView.as_view(), name='rest_login'),
    re_path(r'^login/code/$', views.LoginCodeView.as_view(), name='rest_login_code'),
    re_path(r'^logout/$', views.LogoutView.as_view(), name='rest_logout'),
]
