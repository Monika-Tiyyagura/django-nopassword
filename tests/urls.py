# -*- coding: utf8 -*-
#from django.conf.urls import include, url
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('nopassword.urls')),
    path('accounts-rest/', include('nopassword.rest.urls')),
]

