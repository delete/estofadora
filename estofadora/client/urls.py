#coding: utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('estofadora.client.views',
    url(r'^add/', 'add', name='add'),
)