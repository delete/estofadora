#coding: utf-8
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User

from estofadora.item.tests import create_item, create_picture

from . import TestCase


class HomeViewTest(TestCase):

	def setUp(self):
		user = User.objects.create_user('admin', 'a@a.com', '123')
		self.client = Client()
		self.client.login(username='admin', password='123')
		self.response = self.client.get(reverse('core:home'))

	def tearDown(self):
		self.client.logout()
		
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'index.html')

	def test_get_logout(self):
		self.client.logout()
		self.response = self.client.get(reverse('core:home'))
		self.assertEqual(self.response.status_code, 302)



class SiteViewTest(TestCase):

	def setUp(self):
		self.response = self.client.get(reverse('core:site'))

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'site/site_index.html')

	def test_if_has_login_url(self):
		self.assertContains(self.response, reverse('login:login'))


class PortfolioViewTest(TestCase):

	def setUp(self):
		self.item = create_item(commit=True)
		self.picture1 = create_picture(self.item, public=True)
		self.picture2 = create_picture(self.item, public=True)
		self.picture3 = create_picture(self.item, public=False)

		self.response = self.client.get(reverse('core:portfolio'))

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'site/portfolio.html')

	def test_url_in_content(self):
		# Picture 1 and 2 must appear, because they are public=True
		self.assertContains(self.response, self.item.name)
		self.assertContains(self.response, self.picture1.image.url)
		self.assertContains(self.response, self.picture2.image.url)

		# Picture 3 must not appear, because it is public=False
		self.assertNotContains(self.response, self.picture3.image.url)
