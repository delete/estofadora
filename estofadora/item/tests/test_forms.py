#coding: utf-8
from django.core.files.uploadedfile import SimpleUploadedFile

from estofadora.settings import PATH_TO_IMAGE_TEST

from . import (
	TestCase, make_validated_form, ItemForm, 
	PictureForm, create_item, create_client,
	Picture
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
		form = make_validated_form(name='')
		self.assertTrue(form.errors)

	def test_description_is_not_optional(self):
		form = make_validated_form(description='')
		self.assertTrue(form.errors)


class PictureFormTest(TestCase):

	def test_has_fields(self):
		form = PictureForm()
		existing_fields = list(form.fields.keys())

		expected_fields = [
			'item', 'image'
		]

		self.assertEqual(existing_fields, expected_fields)

	def test_image_is_not_optional(self):
		new_item = create_item(commit=True)
		data = {'item': new_item.pk}
		file_data = {'image': ''}
		form = PictureForm(data, file_data)
		self.assertTrue(form.errors)

	def test_item_is_not_optional(self):
		upload_file = open(PATH_TO_IMAGE_TEST, 'rb')
		data = {'item': ''}
		file_data = {
			'image': SimpleUploadedFile(upload_file.name, upload_file.read())
		}

		form = PictureForm(data, file_data)
		self.assertTrue(form.errors)

	def test_form(self):
		upload_file = open(PATH_TO_IMAGE_TEST, 'rb')
		new_item = create_item(commit=True)
		data = {'item': new_item.pk}
		file_data = {
			'image': SimpleUploadedFile(upload_file.name, upload_file.read())
		}
		
		form = PictureForm(data, file_data)
		self.assertTrue(form.is_valid())
		form.save()
		self.assertTrue(Picture.objects.exists())