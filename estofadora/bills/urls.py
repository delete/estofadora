#coding: utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('estofadora.bills.views',
	url(r'^$', 'new', name='new'),
)