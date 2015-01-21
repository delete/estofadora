from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


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