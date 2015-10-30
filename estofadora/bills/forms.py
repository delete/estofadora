#conding: utf-8
from django import forms
from .models import Bill


class BillForm(forms.ModelForm):

	class Meta:
		model = Bill
		fields = ['name', 'date_to_pay', 'value']

	def __init__(self, *args, **kwargs):
		super(BillForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class': 'form-control'})
		self.fields['date_to_pay'].widget.attrs.update({'class': 'form-control'})
		self.fields['value'].widget.attrs.update({'class': 'form-control'})