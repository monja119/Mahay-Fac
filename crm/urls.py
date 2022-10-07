"""crm0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
import app.views
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^auth/$', app.views.auth),

    # form
    re_path(r'^register/$', app.views.new_user, name='register'),
    re_path(r'^auth/$', app.views.auth, name='authentification'),

    # tab
    re_path(r'^home/$', app.views.home, name='home'),
    re_path(r'profile/', app.views.profile, name='profile'),
    re_path(r'company/', app.views.my_company, name='my_company'),
    re_path(r'create/company', app.views.create_company, name='create_company'),
]
