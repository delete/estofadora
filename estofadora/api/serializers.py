from rest_framework import serializers

from estofadora.client.models import Client
from estofadora.bills.models import Bill
from estofadora.item.models import Item


class ClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bill
		fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = '__all__'