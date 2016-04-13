# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'estofadora.core.views',
    url(r'^$', 'site', name='site'),
    url(r'^inicio/$', 'home', name='home'),
    url(r'^portfolio/$', 'portfolio', name='portfolio'),
    url(r'^contato/$', 'contact', name='contact'),

    url(r'^mensagens/$', 'contactMessages', name='contactMessages'),
    url(r'^(?P<pk>\d+)/remover/', 'deleteMessage', name='deleteMessage'),
    url(r'^(?P<pk>\d+)/lida/', 'markMessageAsRead', name='markMessageAsRead'),
)
