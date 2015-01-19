#coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'estofadora.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^home/', include('estofadora.core.urls', namespace='core')),
    url(r'^cliente/', include('estofadora.client.urls', namespace='client')),
    url(r'^admin/', include(admin.site.urls)),
)
