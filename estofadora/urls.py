#coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'estofadora.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('estofadora.core.urls', namespace='core')),
    url(r'^cliente/', include('estofadora.client.urls', namespace='client')),
    url(r'^item/', include('estofadora.item.urls', namespace='item')),
    url(r'^login/', include('estofadora.login.urls', namespace='login')),
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings
if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(
		settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
	)