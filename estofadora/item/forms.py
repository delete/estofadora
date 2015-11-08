#coding: utf-8
from django import forms
from django.forms.models import inlineformset_factory

from estofadora.client.models import Client

from .models import Item, Picture


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


class PictureForm(forms.ModelForm):

	class Meta:
		model = Picture
		exclude = ['created_at']

	def __init__(self, *args, **kwargs):
		super(PictureForm, self).__init__(*args, **kwargs)
		self.fields['image'].widget.attrs.update({'class': 'form-control'})


PictureFormSet = inlineformset_factory(Item, Picture, fields=('image',))