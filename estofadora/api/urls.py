#coding: utf-8
from django.conf.urls import patterns, url, include

from rest_framework import routers

from .views import ClientViewSet, BillViewSet, ItemViewSet

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'bills', BillViewSet)
router.register(r'items', ItemViewSet)

urlpatterns = patterns('estofadora.api.views',
	url(r'^', include(router.urls)),
)