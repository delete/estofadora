#conding: utf-8
from django.core.urlresolvers import reverse

from . import TestCase, create_client, ClientForm, Client


class AddViewTest(TestCase):

	def setUp(self):
		self.response = self.client.get(reverse('client:add'))

	def tearDown(self):
		pass	

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):		
		self.assertTemplateUsed(self.response, 'client/add.html')

	def test_if_has_form(self):
		form = self.response.context['form']
		self.assertIsInstance(form, ClientForm)

	def test_html(self):
		self.assertContains(self.response, '<form')
		self.assertContains(self.response, '<input', 7)
		self.assertContains(self.response, '<label', 6)
		self.assertContains(self.response, 'type="submit"')
	
	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')


class AddPostTest(TestCase):

	def setUp(self):
		data = create_client()
		self.response = self.client.post(reverse('client:add'), data)

	def tearDown(self):
		Client.objects.all().delete()

	def test_message(self):
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
		self._test_if_got_errors(data)

	def test_post_adress_required(self):
		data = create_client(adress='')
		self._test_if_got_errors(data)

	def test_post_telephone1_required(self):
		data = create_client(telephone1='')
		self._test_if_got_errors(data)

	def test_post_wrong_email(self):
		data = create_client(email='a')
		self._test_if_got_errors(data)

	def _test_if_got_errors(self, data):
		self.response = self.client.post(reverse('client:add'), data)
		self.assertTrue(self.response.context['form'].errors)


class EditViewTest(AddViewTest):

	def setUp(self):
		self.cli = create_client(commit=True)
		self.response = self.client.get(reverse('client:edit', args=[self.cli.pk]))

	def tearDown(self):
		Client.objects.all().delete()

	def test_template(self):
		self.assertTemplateUsed(self.response, 'client/edit.html')


class EditPostTest(TestCase):

	def setUp(self):
		self.cli = create_client(commit=True)

	def tearDown(self):
		Client.objects.all().delete()

	def test_post_name(self):
		self.cli.name = 'Fellipe'
		self.cli.save()
		self.response = self.client.post(reverse('client:edit', args=[self.cli.pk]))
		self.assertEqual(Client.objects.first().name, 'Fellipe')

	def test_post_adress(self):
		self.cli.adress = 'Rua b'
		self.cli.save()
		self.response = self.client.post(reverse('client:edit', args=[self.cli.pk]))
		self.assertEqual(Client.objects.first().adress, 'Rua b')

	def test_post_email(self):
		self.cli.email = 'fe@email.com'
		self.cli.save()
		self.response = self.client.post(reverse('client:edit', args=[self.cli.pk]))
		self.assertEqual(Client.objects.first().email, 'fe@email.com')

	def test_post_telephone1(self):
		self.cli.telephone1 = '456'
		self.cli.save()
		self.response = self.client.post(reverse('client:edit', args=[self.cli.pk]))
		self.assertEqual(Client.objects.first().telephone1, '456')

	def test_post_telephone2(self):
		self.cli.telephone2 = '678'
		self.cli.save()
		self.response = self.client.post(reverse('client:edit', args=[self.cli.pk]))
		self.assertEqual(Client.objects.first().telephone2, '678')

	def test_post_is_active(self):
		self.cli.is_active = False
		self.cli.save()
		self.response = self.client.post(reverse('client:edit', args=[self.cli.pk]))
		self.assertEqual(Client.objects.first().is_active, False)


class EditInvalidPostTest(AddInvalidPostTest):

	def setUp(self):
		self.cli = create_client(commit=True)

	def tearDown(self):
		Client.objects.all().delete()

	def _test_if_got_errors(self, data):
		self.response = self.client.post(reverse('client:edit', args=[self.cli.pk]))
		self.assertTrue(self.response.context['form'].errors)


class ListViewTest(TestCase):

	def setUp(self):
		self.client1 = create_client(commit=True)
		self.client2 = create_client(commit=True, name='Andre', email='a@email.com')

		self.response = self.client.get(reverse('client:list'))

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'client/list.html')

	def test_if_contains_clients(self):
		self.assertContains(self.response, self.client1.name)
		self.assertContains(self.response, self.client2.name)


class DeleteViewTest(TestCase):

	def setUp(self):
		self.client1 = create_client(commit=True)
		self.client2 = create_client(commit=True, name='Andre', email='a@email.com')

		self.response = self.client.post(reverse('client:delete', args=[self.client1.pk]), follow=True)
	
	def tearDown(self):
		Client.objects.all().delete()

	def test_redirected(self):
		expected_url = reverse('client:list')
		
		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)

	def test_if_deleted(self):
		self.assertEqual(len(Client.objects.all()), 1)

	def test_message(self):
		self.assertContains(self.response, 'Cliente removido com sucesso!')


