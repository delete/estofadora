# conding: utf-8

from . import TestCase, make_validated_form, ContactForm


class ContactFormTest(TestCase):

    def test_if_has_fields(self):
        form = ContactForm()
        existing_fields = list(form.fields.keys())

        expected_field = [
            'name', 'email', 'telephone', 'subject', 'description'
        ]

        self.assertEqual(existing_fields, expected_field)

    def test_email_or_telephone(self):
        '''
            Must input at leat one option of contact: email or telephone
        '''
        form = make_validated_form(email='', telephone='')
        self.assertTrue(form.errors)

    def test_email_is_optional(self):
        form = make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_telephone_is_optional(self):
        form = make_validated_form(telephone='')
        self.assertFalse(form.errors)

    def test_name_is_not_optional(self):
        form = make_validated_form(name='')
        self.assertTrue(form.errors)

    def test_subject_is_not_optional(self):
        form = make_validated_form(subject='')
        self.assertTrue(form.errors)

    def test_description_is_not_optional(self):
        form = make_validated_form(description='')
        self.assertTrue(form.errors)

    def test_form(self):
        form = make_validated_form()
        self.assertFalse(form.errors)
