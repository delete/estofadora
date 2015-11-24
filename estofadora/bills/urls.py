#coding: utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('estofadora.bills.views',
	url(r'^$', 'new', name='new'),
	url(r'^listar/$', 'list', name='list'),
	url(r'^(?P<pk>\d+)/remover/', 'delete', name='delete'),
)