#coding: utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('estofadora.statement.views',
	url(r'^$', 'home', name='home'),
	url(r'^caixa/$', 'cash', name='cash'),
	url(r'^caixa-mensal/$', 'cash_month', name='cash_month'),
	url(r'^caixa-anual/$', 'cash_annual', name='cash_annual'),
	url(r'^caixa/(?P<pk>\d+)/remover/', 'delete', name='delete'),
	url(r'^caixa/(?P<pk>\d+)/editar/', 'edit', name='edit'),
)