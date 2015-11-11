# coding: utf-8
import os

from django.db import IntegrityError, transaction
from . import TestCase, Item, create_item, create_picture, Picture


class ItemModelTest(TestCase):

	def setUp(self):		
		self.item = create_item(commit=True)
		
	def tearDown(self):
		Item.objects.all().delete()

	def test_if_item_is_not_concluded(self):
		self.assertFalse(self.item.concluded)

	def test_rest_value(self):
		self.assertEqual(self.item.rest_value(), 500)


class PictureModelTest(TestCase):

	def setUp(self):
		self.item = create_item(commit=True)
		self.picture = create_picture(self.item)

	def test_if_created(self):
		self.assertTrue(Picture.objects.exists())

	def test_amount(self):
		self.assertEqual(len(Picture.objects.all()), 1)
	
	def test_if_image_was_created(self):
		self.assertTrue(self.picture.image)

	def test_if_image_file_was_created(self):
		self.assertTrue(os.path.exists(self.picture.image.path))

	def test_if_image_file_was_deleted(self):
		path = self.picture.image.path
		self.picture.delete()
		self.assertFalse(os.path.exists(path))

	def test_if_public_is_false(self):
		''' Public must be False as default '''
		self.assertFalse(self.picture.public)

	def test_if_state_is_before(self):
		''' State must be 'berofe' as default '''
		self.assertEqual(self.picture.state, 'before')