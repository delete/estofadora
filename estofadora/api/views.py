from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from estofadora.client.models import Client
from estofadora.bills.models import Bill
from estofadora.item.models import Item

from .serializers import (
	ClientSerializer, BillSerializer, ItemSerializer
)


class ClientViewSet(viewsets.ModelViewSet):
	"""
		API endpoint that allows clients to be viewed or edited.
	"""
	permission_classes = (IsAuthenticated,)

	queryset = Client.objects.all().order_by('-date_join')
	serializer_class = ClientSerializer


class BillViewSet(viewsets.ModelViewSet):
	"""
		API endpoint that allows clients to be viewed or edited.
	"""
	permission_classes = (IsAuthenticated,)
	
	queryset = Bill.objects.all().order_by('-date_to_pay')
	serializer_class = BillSerializer


class ItemViewSet(viewsets.ModelViewSet):
	"""
		API endpoint that allows clients to be viewed or edited.
	"""
	permission_classes = (IsAuthenticated,)
	
	queryset = Item.objects.all()
	serializer_class = ItemSerializer