#coding: utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('estofadora.core.views',
    url(r'^$', 'home', name='home'),
)