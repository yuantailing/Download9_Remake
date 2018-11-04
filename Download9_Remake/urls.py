"""Download9_Remake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path
from Download9 import views as download9_views

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'^index/?$', download9_views.login),
    re_path(r'^check_login/?$', download9_views.check_login),
    re_path(r'^not_exist/?$', download9_views.not_exist),
    re_path(r'^$', download9_views.index),
    re_path(r'^.*$', download9_views.jump_to_not_exist),
]
