"""rsclub_portal URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rsapi import views
from django.contrib.staticfiles import views as sviews
from login import views as lviews

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test$', views.index, name='index'),
    url(r'^domains/*', include('domainlist.urls')),
    url(r'^static/(?P<path>.*)$', sviews.serve),
    url(r'^/*$', lviews.login_page),
    url(r'^login/*', lviews.do_login)
]
