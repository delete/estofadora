#conding: utf-8
from django.core.urlresolvers import reverse

from . import TestBase


class StatementViewTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('statement:home')
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):		
		self.assertTemplateUsed(self.response, 'statement/statement.html')
	
	def test_get_logout(self):
		self._test_get_logout(self.url)

	def test_html(self):
		self.assertContains(self.response, 'Financeiro')
	