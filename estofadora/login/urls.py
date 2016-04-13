# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'estofadora.login.views.login', name='login'),
    # url(r'^$', 'django.contrib.auth.views.login',
    #   {'template_name': 'login.html'}, name='login'),

    url(r'^sair/$', 'django.contrib.auth.views.logout',
        {'next_page': 'login:login'}, name='logout'),

)
