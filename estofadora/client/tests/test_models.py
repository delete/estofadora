# coding: utf-8
from django.db import IntegrityError, transaction

from . import TestCase, Client, create_client


class ClientModelTest(TestCase):

	def setUp(self):
		data = create_client()
		self.client = Client.objects.create(**data)
		
	def tearDown(self):
		Client.objects.all().delete()

	def test_if_client_is_active(self):
		self.assertTrue(self.client.is_active)
	
	def test_duplicate_email(self):
		with transaction.atomic():
			data = create_client(name='Andre')
			c = Client(**data)
			self.assertRaises(IntegrityError, c.save)

		self.assertEqual(len(Client.objects.all()), 1)
