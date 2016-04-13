# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'estofadora.bills.views',
    url(r'^$', 'new', name='new'),
    url(r'^listar/$', 'list', name='list'),
    url(r'^(?P<pk>\d+)/remover/', 'delete', name='delete'),
    url(r'^(?P<pk>\d+)/pago/', 'mark_as_paid', name='mark_as_paid'),
)
