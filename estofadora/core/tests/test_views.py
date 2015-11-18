#coding: utf-8
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User

from estofadora.item.tests import create_item, create_picture

from . import TestCase, ContactForm, Contact, create_contact


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
		self.item = create_item(commit=True)
		self.picture1 = create_picture(self.item, public=True, state='after')
		self.picture2 = create_picture(self.item, public=True, state='after')
		self.picture3 = create_picture(self.item, public=True, state='after')
		self.picture4 = create_picture(self.item, public=True, state='after')
		self.picture5 = create_picture(self.item, public=True)

		self.response = self.client.get(reverse('core:site'))

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'site/site_index.html')

	def test_if_has_login_url(self):
		self.assertContains(self.response, reverse('login:login'))

	def test_url_in_content(self):
		# Picture 1,2,3 and 4 must appear, because they are public=True
		self.assertContains(self.response, self.picture1.image.url)
		self.assertContains(self.response, self.picture2.image.url)
		self.assertContains(self.response, self.picture3.image.url)
		self.assertContains(self.response, self.picture4.image.url)

		# Picture 5 must not appear, because it is public=False
		self.assertNotContains(self.response, self.picture5.image.url)


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


class ContactViewTest(TestCase):

	def setUp(self):
		self.response = self.client.get(reverse('core:contact'))

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'site/contact.html')

	def test_context(self):
		self.assertContains(self.response, '<iframe')

	def test_if_has_form(self):
		form = self.response.context['form']
		self.assertIsInstance(form, ContactForm)

	def test_html(self):
		self.assertContains(self.response, '<form')
		self.assertContains(self.response, '<input', 5)
		self.assertContains(self.response, 'type="submit"')


class ContactPostTest(TestCase):

	def setUp(self):
		data = create_contact(commit=False)
		self.response = self.client.post(
				reverse('core:contact'), data, follow=True
			)

	def test_message(self):
		self.assertContains(self.response, 'Obrigado pela mensagem, entraremos em contato!')

	def test_if_saved(self):
		self.assertTrue(Contact.objects.exists())

	def test_redirect(self):
		expected_url = reverse('core:contact')

		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)


class ContactMessagesViewTest(TestCase):

	def setUp(self):
		user = User.objects.create_user('admin', 'a@a.com', '123')
		self.client = Client()
		self.client.login(username='admin', password='123')

		self.contactMessage = create_contact(commit=True)

		self.response = self.client.get(reverse('core:contactMessages'))

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'contactMessages.html')

	def test_get_logout(self):
		self.client.logout()
		self.response = self.client.get(reverse('core:home'))
		self.assertEqual(self.response.status_code, 302)

	def test_content(self):
		self.assertContains(self.response, self.contactMessage.name)
		self.assertContains(self.response, self.contactMessage.subject)
		self.assertContains(self.response, self.contactMessage.email)
		self.assertContains(self.response, self.contactMessage.telephone)
		self.assertContains(self.response, self.contactMessage.description)

	def test_empty(self):
		Contact.objects.all().delete()
		
		self.response = self.client.get(reverse('core:contactMessages'))		
		self.assertContains(self.response, 'Nenhuma mensagem!')


class DeleteMensagemViewTest(TestCase):

	def setUp(self):
		user = User.objects.create_user('admin', 'a@a.com', '123')
		self.client = Client()
		self.client.login(username='admin', password='123')

		self.contactMessage1 = create_contact(commit=True)

		self.contactMessage2 = create_contact(commit=True)

		#Must have 2 messages before post.
		self.assertEqual(len(Contact.objects.all()), 2)
		
		self.response = self.client.post(reverse('core:deleteMessage', args=[self.contactMessage1.pk]), follow=True)
	
	def test_redirect(self):
		expected_url = reverse('core:contactMessages')

		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)

	def test_if_deleted(self):
		self.assertEqual(len(Contact.objects.all()), 1)

	def test_message(self):
		self.assertContains(self.response, 'Mensagem removida com sucesso!')