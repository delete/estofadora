from django.test import TestCase
from django.test.client import Client


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