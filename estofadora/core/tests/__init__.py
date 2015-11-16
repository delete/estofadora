#coding: utf-8
import datetime

from django.test import TestCase

from estofadora.core.forms import ContactForm
from estofadora.core.models import Contact


def make_validated_form(commit=True, **kwargs):
	data = {
		'name': 'MyName',
		'email': 'myemai@email.com',
		'telephone': '11111111',
		'subject': 'About',
		'description': 'Was bad, but now, is good.',
	}
	data.update(kwargs)
	if commit:
		form = ContactForm(data)
		form.is_valid()
		return form
	else:
		return data


def create_contact(commit=False, **kwargs):
	data = {
		'name': 'MyName',
		'email': 'myemai@email.com',
		'telephone': '11111111',
		'subject': 'About',
		'description': 'Was bad, but now, is good.',
	}
	data.update(kwargs)	
	if commit:
		return Contact.objects.create(**data)
	
	return data