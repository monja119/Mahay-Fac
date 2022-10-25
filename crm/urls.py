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

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^auth/$', app.views.auth),
    re_path(r'^$', app.views.home),

    # form
    re_path(r'^register/$', app.views.new_user, name='register'),
    re_path(r'^auth/$', app.views.auth, name='authentification'),

    # tab
    re_path(r'^home/$', app.views.home, name='home'),
    re_path(r'^profile/$', app.views.profile, name='profile'),
    re_path(r'^company/', app.views.my_company, name='my_company'),
    re_path(r'^client/', app.views.client, name='client'),

    # creation
    re_path(r'^create/company', app.views.create_company, name='create_company'),
    re_path(r'^create/client', app.views.create_client, name='create_client'),
    re_path(r'^create/invoice', app.views.create_invoice, name='create_invoice'),

    # check
    re_path(r'check/(?P<arg>)$', app.views.check, name='check'),
    re_path(r'check/', app.views.home, name='check'),

    # remove
    re_path(r'remove/(?P<arg>)$', app.views.remove, name='remove'),

    re_path(r'search/', app.views.search, name='search'),

    re_path(r'^export/(?P<id>)', app.views.export, name='export'),
]