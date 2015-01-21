# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'django.contrib.auth.views.login',
    	{'template_name': 'login.html'}, name='login'),

 	url(r'^sair/$', 'django.contrib.auth.views.logout',
    	{'next_page': 'login:login'}, name='logout'),

)
