#coding: utf-8

from . import TestCase, make_validated_form, ItemForm

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
