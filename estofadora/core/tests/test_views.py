#coding: utf-8
from django.core.urlresolvers import reverse
from . import TestCase


class HomeGetTest(TestCase):

	def setUp(self):
		self.response = self.client.get(reverse('core:home'))

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'index.html')