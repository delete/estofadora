# coding: utf-8

from . import TestCase, make_validated_form, CashForm


class CashFormTest(TestCase):

	def test_if_has_fields(self):
		form = CashForm()
		existing_fields = list(form.fields.keys())

		expected_field = ['date', 'history', 'income', 'expenses']

		self.assertEqual(existing_fields, expected_field)

	def test_date_is_not_optional(self):
		form = make_validated_form(date='')
		self.assertTrue(form.errors)

	def test_history_is_not_optional(self):
		form = make_validated_form(history='')
		self.assertTrue(form.errors)

	def test_income_is_not_optional(self):
		form = make_validated_form(income='')
		self.assertTrue(form.errors)

	def test_expenses_is_not_optional(self):
		form = make_validated_form(expenses='')
		self.assertTrue(form.errors)

	def test_form(self):
		form = make_validated_form()
		self.assertFalse(form.errors)