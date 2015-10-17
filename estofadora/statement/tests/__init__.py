from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client


class TestBase(TestCase):

	def _create_user(self):
		user = User.objects.create_user('admin', 'a@a.com', '123')
		return user

	def login(self, username='admin', password='123'):
		self._create_user()
		self.client = Client()
		self.client.login(username=username, password=password)
	
	def logout(self):
		self.client.logout()

	def tearDown(self):
		self.logout()
		User.objects.all().delete()

	def _test_get_logout(self, url):
		self.logout()
		self.response = self.client.get(url)
		self.assertEqual(self.response.status_code, 302)