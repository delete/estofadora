from django.test import TestCase
from django.test.client import Client

from estofadora.client.forms import ClientForm


def create_client(**kwargs):
	data = {
		'name': 'Fellipe',
		'email': 'email@email.com',
		'adress': 'Street',
		'telephone1': '123',
		'telephone2': '321',
	}
	data.update(kwargs)	
	
	return data


def make_validated_form(**kwargs):
    data = {
		'name': 'Fellipe',
		'email': 'email@email.com',
		'adress': 'Street',
		'telephone1': '123',
		'telephone2': '321',
    }
    data.update(kwargs)
    form = ClientForm(data)
    form.is_valid()
    return form