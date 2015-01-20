from django.core.urlresolvers import reverse

from . import TestCase, create_client, ClientForm, Client


class AddViewTest(TestCase):

	def setUp(self):
		self.response = self.client.get(reverse('client:add'))

	def tearDown(self):
		pass	

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_if_has_form(self):
		form = self.response.context['form']
		self.assertIsInstance(form, ClientForm)

	def test_html(self):
		self.assertContains(self.response, '<form')
		self.assertContains(self.response, '<input', 6)
		self.assertContains(self.response, '<label', 5)
		self.assertContains(self.response, 'type="submit"')
	
	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')


class AddPostTest(TestCase):

	def setUp(self):
		data = create_client()
		self.response = self.client.post(reverse('client:add'), data)

	def tearDown(self):
		Client.objects.all().delete()

	def test_post(self):
		self.assertContains(self.response, 'Cliente cadastrado com sucesso!')

	def test_save(self):
		self.assertTrue(Client.objects.exists())


class AddInvalidPostTest(TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_post_name_required(self):
		data = create_client(name='')
		self.response = self.client.post(reverse('client:add'), data)
		self.assertTrue(self.response.context['form'].errors)

	def test_post_adress_required(self):
		data = create_client(adress='')
		self.response = self.client.post(reverse('client:add'), data)
		self.assertTrue(self.response.context['form'].errors)

	def test_post_telephone1_required(self):
		data = create_client(telephone1='')
		self.response = self.client.post(reverse('client:add'), data)
		self.assertTrue(self.response.context['form'].errors)

	def test_post_wrong_email(self):
		data = create_client(email='a')
		self.response = self.client.post(reverse('client:add'), data)
		self.assertTrue(self.response.context['form'].errors)