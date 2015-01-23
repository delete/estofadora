#coding: utf-8

from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
	
	class Meta:
		model = Item
		fields = [
			'client', 'name', 'description', 'concluded',
			'delivery_date', 'total_value', 'total_paid',
		]