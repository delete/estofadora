from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient

from estofadora.client.models import Client as ModelClient
from estofadora.bills.models import Bill
from estofadora.item.models import Item

from estofadora.client.tests import create_client
from estofadora.bills.tests import create_bill
from estofadora.item.tests import create_item


class TestBase(APITestCase):
	
	def _create_user(self):
		user = User.objects.create_user('admin', 'a@a.com', '123')
		return user

	def login(self, username='admin', password='123'):
		self._create_user()
		self.client = APIClient()
		self.client.login(username=username, password=password)
	
	def logout(self):
		self.client.logout()

	def tearDown(self):
		self.logout()
		ModelClient.objects.all().delete()
		User.objects.all().delete()
		Bill.objects.all().delete()
		Item.objects.all().delete()
