#coding: utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('estofadora.item.views',
    url(r'^add/$', 'add', name='add'),
    url(r'^(?P<pk>\d+)/editar/', 'edit', name='edit'),
    url(r'^listar/$', 'list', name='list'),
    url(r'^(?P<pk>\d+)/remover/', 'delete', name='delete'),

    url(r'^(?P<pk>\d+)/imagens/', 'image_list', name='image_list'),
    url(r'^imagens/(?P<pk>\d+)/remover/', 'image_delete', name='image_delete'),
)