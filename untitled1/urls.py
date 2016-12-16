"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from wallet.views import user_profile,add_money,subtract_money, update_profile, transaction

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^create_user/$', views.create_user),
    url(r'^accounts/profile/$', user_profile),
    url(r'^add_money/$', add_money),
    url(r'subtract_money/$', subtract_money),
    url(r'^update_profile/$', update_profile),
    url(r'^trans/$', transaction),
    url(r'^home/$', views.home)
]
