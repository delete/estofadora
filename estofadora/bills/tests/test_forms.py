# coding: utf-8

from . import TestCase, make_validated_form, BillForm, create_bill


class BillFormTest(TestCase):

    def test_if_has_fields(self):
        form = BillForm()
        existing_fields = list(form.fields.keys())

        expected_field = ['name', 'date_to_pay', 'value']

        self.assertEqual(existing_fields, expected_field)

    def test_date_to_pay_is_not_optional(self):
        form = make_validated_form(date_to_pay='')
        self.assertTrue(form.errors)

    def test_name_is_not_optional(self):
        form = make_validated_form(name='')
        self.assertTrue(form.errors)

    def test_value_is_not_optional(self):
        form = make_validated_form(value='')
        self.assertTrue(form.errors)

    def test_same_name_and_date_error(self):
        # Must have only one bill created with the same name and date.
        create_bill()
        form = make_validated_form()
        self.assertTrue(form.errors)

    def test_form(self):
        form = make_validated_form()
        self.assertFalse(form.errors)
