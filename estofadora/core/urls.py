#coding: utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('estofadora.core.views',
    url(r'^$', 'site', name='site'),
    url(r'^inicio/$', 'home', name='home'),
    url(r'^portfolio/$', 'portfolio', name='portfolio'),
)