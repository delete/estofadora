# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^sair/$', 'django.contrib.auth.views.logout',
        {'next_page': 'login:login'}, name='logout'),
    url(r'^$', 'estofadora.login.views.login', name='login'),
)
