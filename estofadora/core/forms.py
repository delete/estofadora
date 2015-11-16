#conding: utf-8
from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
	
	class Meta:
		model = Contact
		fields = ['name', 'email', 'telephone', 'subject', 'description']

	def clean(self):
		cleaned_data = super(ContactForm, self).clean()

		email = cleaned_data.get('email')
		telephone = cleaned_data.get('telephone')

		if not email and not telephone:
			raise forms.ValidationError(
				'Por favor, entre com pelo menos uma opção de contato. Email ou telefone.'
			)

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nome completo'})
		self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seu email'})
		self.fields['telephone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seu telefone com DDD'})
		self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Assunto da mensagem'})
		self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Sua mensagem'})