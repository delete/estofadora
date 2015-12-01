#coding: utf-8
from django.core.files.uploadedfile import SimpleUploadedFile

from estofadora.settings.base import PATH_TO_IMAGE_TEST

from . import (
	TestCase, make_validated_item_form, ItemForm,
	ItemPictureForm, make_validated_item_picture_form,
	PictureForm
)


class ItemFormTest(TestCase):

	def test_if_has_fields(self):
		form = ItemForm()
		existing_fields = list(form.fields.keys())

		expected_fields = [
			'client', 'name', 'delivery_date', 'total_value',
			'total_paid', 'description', 'concluded',
			  
		]

		self.assertEqual(existing_fields, expected_fields)

	def test_name_is_not_optional(self):
		form = make_validated_item_form(name='')
		self.assertTrue(form.errors)

	def test_description_is_not_optional(self):
		form = make_validated_item_form(description='')
		self.assertTrue(form.errors)


class ItemPictureFormTest(ItemFormTest):

	def test_if_has_fields(self):
		form = ItemPictureForm()
		existing_fields = list(form.fields.keys())

		expected_fields = [
			'client', 'name', 'delivery_date', 'total_value',
			'total_paid', 'description', 'concluded', 'files'
		]

		self.assertEqual(existing_fields, expected_fields)

	def test_files_is_optional(self):
		form = make_validated_item_picture_form(files='')
		self.assertFalse(form.errors)

	def test_form(self):
		data = make_validated_item_picture_form(commit=False)
		
		with open(PATH_TO_IMAGE_TEST, 'rb') as img:
			data['files'] = img

		form = ItemPictureForm(data)
		self.assertTrue(form.is_valid())


class PictureFormTest(TestCase):

	def test_if_has_fields(self):
		form = PictureForm()
		existing_fields = list(form.fields.keys())

		expected_fields = ['files']

		self.assertEqual(existing_fields, expected_fields)

	def test_files_is_not_optional(self):
		data = {
			'files': ''
		}
		form = PictureForm(data)
		self.assertTrue(form.errors)
