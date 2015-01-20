#conding: utf-8
from django import forms
from .models import Client


class ClientForm(forms.ModelForm):

	class Meta:
		model = Client
		fields = ['name', 'adress', 'email', 'telephone1', 'telephone2']