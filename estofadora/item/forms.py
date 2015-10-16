#coding: utf-8

from django import forms
from .models import Item
from estofadora.client.models import Client

class ItemForm(forms.ModelForm):
	client = forms.ModelChoiceField(
		queryset=Client.objects.all(), label="Cliente")
	description = forms.CharField(label="Descrição", widget=forms.Textarea)
	
	class Meta:
		model = Item
		fields = [
			'client', 'name', 'delivery_date',
			'total_value', 'total_paid', 'description', 'concluded'
		]
	
	def __init__(self, *args, **kwargs):
		super(ItemForm, self).__init__(*args, **kwargs)
		self.fields['client'].widget.attrs.update({'class': 'form-control'})
		self.fields['name'].widget.attrs.update({'class': 'form-control'})
		self.fields['description'].widget.attrs.update({'class': 'form-control'})
		self.fields['delivery_date'].widget.attrs.update({'class': 'form-control'})
		self.fields['total_value'].widget.attrs.update({'class': 'form-control'})
		self.fields['total_paid'].widget.attrs.update({'class': 'form-control'})