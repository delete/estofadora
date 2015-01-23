# coding: utf-8
from django.db import IntegrityError, transaction
from . import TestCase, Item, create_item


class ItemModelTest(TestCase):

	def setUp(self):		
		self.item = create_item(commit=True)
		
	def tearDown(self):
		Item.objects.all().delete()

	def test_if_item_is_not_concluded(self):
		self.assertFalse(self.item.concluded)

	def test_rest_value(self):
		self.assertEqual(self.item.rest_value(), 500)
