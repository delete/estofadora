#coding: utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('estofadora.statement.views',
	url(r'^$', 'home', name='home'),
	url(r'^caixa/$', 'cash', name='cash'),
	url(r'^(?P<pk>\d+)/remover/', 'delete', name='delete'),
)