# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'estofadora.client.views',
    url(r'^(?P<pk>\d+)/editar/', 'edit', name='edit'),
    url(r'^listar/$', 'list', name='list'),
    url(r'^(?P<pk>\d+)/remover/', 'delete', name='delete'),
    url(r'^(?P<pk>\d+)/itens/', 'list_items', name='list_items'),
    url(r'^$', 'add', name='add'),
)
