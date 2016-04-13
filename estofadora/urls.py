# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'estofadora.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('estofadora.core.urls', namespace='core')),
    url(r'^cliente/', include('estofadora.client.urls', namespace='client')),
    url(r'^item/', include('estofadora.item.urls', namespace='item')),
    url(r'^login/', include('estofadora.login.urls', namespace='login')),
    url(
        r'^relatorios/',
        include('estofadora.statement.urls', namespace='statement')
    ),
    url(r'^contas/', include('estofadora.bills.urls', namespace='bills')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^api/', include('estofadora.api.urls', namespace='api')),
)


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
