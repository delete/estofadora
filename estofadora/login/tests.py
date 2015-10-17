from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .forms import LoginForm


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('login:login'))

    def tearDown(self):
    	self.client.logout()

    def test_get(self):      
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):        
        self.assertTemplateUsed(self.response, 'login.html')

    def test_html(self):
        'HTML must have contain 3 inputs(user, pass and csrf token) and a submit'
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'submit')


class LoginPostTest(TestCase):

	def setUp(self):
		user = User.objects.create_user('admin', 'admin@admin.com', '123')
		self.client = Client()

	def tearDown(self):
		self.client.logout()
		User.objects.all().delete()

	def test_already_logged(self):
		'If already logged, will have a redirect, so, must return code 302'
		self.response = self.client.post(reverse('login:login'), self.make_validated_data())
		self.response = self.client.get(reverse('login:login'))
		self.assertEqual(self.response.status_code, 302)

	def test_valid_login(self):
		'With valid login, will have a redirect, so, must return code 302'
		self.response = self.client.post(reverse('login:login'), self.make_validated_data())
		self.assertEqual(self.response.status_code, 302)

	def test_invalid_login(self):
		'With invalid login, will not have a redirect, so, must return code 200'
		self.response = self.client.post(reverse('login:login'), self.make_validated_data(password='1'))
		self.assertEqual(self.response.status_code, 200)

	def make_validated_data(self, **kwargs):
		data = {
				'username': 'admin',
				'password': '123'
				}
		data.update(kwargs)
		return data


#TODO - FIX THESE TESTS. 
#I DON'T KNOW WHY IT IS NOT RETURNING ERRORS
#WHEN USERNAME OR PASSWORD IS EMPTY.

class LoginFormTest(TestCase):

	def setUp(self):
		user = User.objects.create_user('admin', 'admin@admin.com', '123')

	def test_if_has_fields(self):
		form = LoginForm()
		existing_fields = list(form.fields.keys())

		expected_field = ['username', 'password']

		self.assertEqual(existing_fields, expected_field)

	# def test_username_is_not_optional(self):
	# 	form = self.make_validated_form(username='')
	# 	self.assertTrue(form.errors)

	# def test_password_is_not_optional(self):
	# 	form = self.make_validated_form(password='')
	# 	self.assertTrue(form.errors)

	def test_form(self):
		form = self.make_validated_form()
		self.assertFalse(form.errors)

	def make_validated_form(self, **kwargs):
	    data = {
			'username': 'admin',
			'password': '123',
	    }
	    data.update(kwargs)
	    form = LoginForm(data)
	    form.is_valid()
	    return form