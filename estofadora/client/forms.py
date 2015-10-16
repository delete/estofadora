#conding: utf-8
from django import forms
from .models import Client


class ClientForm(forms.ModelForm):

	class Meta:
		model = Client
		fields = ['name', 'adress', 'email', 'telephone1', 'telephone2', 'is_active']

	def __init__(self, *args, **kwargs):
		super(ClientForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class': 'form-control'})
		self.fields['adress'].widget.attrs.update({'class': 'form-control'})
		self.fields['email'].widget.attrs.update({'class': 'form-control'})
		self.fields['telephone1'].widget.attrs.update({'class': 'form-control'})
		self.fields['telephone2'].widget.attrs.update({'class': 'form-control'})