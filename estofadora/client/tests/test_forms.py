# coding: utf-8

from . import TestCase, make_validated_form, ClientForm


class ClientFormTest(TestCase):

    def test_if_has_fields(self):
        form = ClientForm()
        existing_fields = list(form.fields.keys())

        expected_field = [
            'name', 'adress', 'email', 'telephone1', 'telephone2', 'is_active'
        ]

        self.assertEqual(existing_fields, expected_field)

    def test_email_is_optional(self):
        form = make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_telephone2_is_optional(self):
        form = make_validated_form(telephone2='')
        self.assertFalse(form.errors)

    def test_name_is_not_optional(self):
        form = make_validated_form(name='')
        self.assertTrue(form.errors)

    def test_telephone1_is_not_optional(self):
        form = make_validated_form(telephone1='')
        self.assertTrue(form.errors)

    def test_form(self):
        form = make_validated_form()
        self.assertFalse(form.errors)
