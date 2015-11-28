#conding: utf-8
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet

from estofadora.item.tests import create_item, create_picture
from estofadora.item.models import Item, Picture

from . import create_client, ClientForm, ModelClient, TestBase


class AddViewTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('client:add')
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_get_logout(self):
		self._test_get_logout(self.url)

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


class AddPostTest(TestBase):

	def setUp(self):
		self.login()
		data = create_client()
		self.response = self.client.post(
				reverse('client:add'), data, follow=True
			)

	def test_message(self):
		self.assertContains(self.response, 'Cliente cadastrado com sucesso!')

	def test_if_saved(self):
		self.assertTrue(ModelClient.objects.exists())

	def test_redirect(self):
		expected_url = reverse('client:list')

		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)


class AddInvalidPostTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('client:add')

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
		self.response = self.client.post(self.url, data)
		self.assertTrue(self.response.context['form'].errors)


class EditViewTest(AddViewTest):

	def setUp(self):
		self.login()
		self.cli = create_client(commit=True)
		self.url = reverse('client:edit', args=[self.cli.pk])
		self.response = self.client.get(self.url)

	def tearDown(self):
		ModelClient.objects.all().delete()

	def test_template(self):
		self.assertTemplateUsed(self.response, 'client/edit.html')


class EditPostTest(TestBase):

	def setUp(self):
		self.login()
		self.cli = create_client(commit=True)
		self.url = reverse('client:edit', args=[self.cli.pk])
		self.response = self.client.get(self.url)

		self.form = self.response.context['form']
		self.data = self.form.initial

	def test_post_name(self):
		self.data['name'] = 'Fellipe Pinheiro'

		self.__post(self.data)
		self.assertEqual(ModelClient.objects.first().name, 'Fellipe Pinheiro')

	def test_post_adress(self):
		self.data['adress'] = 'Rua b'

		self.__post(self.data)
		self.assertEqual(ModelClient.objects.first().adress, 'Rua b')

	def test_post_email(self):
		self.data['email'] = 'fe@email.com'
		
		self.__post(self.data)
		self.assertEqual(ModelClient.objects.first().email, 'fe@email.com')

	def test_post_telephone1(self):
		self.data['telephone1'] = '456'
		
		self.__post(self.data)
		self.assertEqual(ModelClient.objects.first().telephone1, '456')

	def test_post_telephone2(self):
		self.data['telephone2'] = '678'
		
		self.__post(self.data)
		self.assertEqual(ModelClient.objects.first().telephone2, '678')

	def test_post_is_active(self):
		self.data['is_active'] = False
		
		self.__post(self.data)
		self.assertEqual(ModelClient.objects.first().is_active, False)

	def __post(self, data):
		response = self.client.post(self.url, data, follow=True)
		self.__test_redirected(response)

	def __test_redirected(self, response):
		expected_url = reverse('client:list')
		
		self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


class EditInvalidPostTest(TestBase):

	def setUp(self):
		self.login()
		self.cli = create_client(commit=True)
		self.url = reverse('client:edit', args=[self.cli.pk])
		self.response = self.client.get(self.url)

		self.form = self.response.context['form']
		self.data = self.form.initial	

	def test_post_name_required(self):
		self.data['name'] = ''

		self._test_if_got_errors()
		
	def test_post_adress_required(self):
		self.data['adress'] = ''
		
		self._test_if_got_errors()

	def test_post_email_required(self):
		self.data['email'] = 'a'
		
		self._test_if_got_errors()

	def test_post_telephone1_required(self):
		self.data['telephone1'] = ''
		
		self._test_if_got_errors()

	def test_post_telephone2_is_not_required(self):
		self.data['telephone1'] = ''
		
		self._test_if_got_errors()	

	def _test_if_got_errors(self):
		self.response = self.client.post(self.url, self.data)
		self.assertTrue(self.response.context['form'].errors)


class ListViewTest(TestBase):

	def setUp(self):
		self.login()
		self.client1 = create_client(commit=True)
		self.client2 = create_client(commit=True, name='Andre', email='a@email.com')

		self.url = reverse('client:list')
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'client/list.html')

	def test_if_contains_clients(self):
		self.assertContains(self.response, self.client1.name)
		self.assertContains(self.response, self.client2.name)

	def test_empty(self):
		ModelClient.objects.all().delete()

		self.response = self.client.get(self.url)
				
		expected = 'Nenhum cliente encontrado.'
		self.assertContains(self.response, expected)

	def test_context(self):
		# + 1 csrf
		self.assertContains(self.response, '<input', 2)
		self.assertContains(self.response, 'submit', 1)

	def test_post(self):
		data = {'name':'Andre'}
		self.response = self.client.post(self.url, data)
		self.assertContains(self.response, self.client2.name)
		self.assertContains(self.response, self.client2.email)

		#client1 items should not appear
		self.assertNotContains(self.response, self.client1.name)
		self.assertNotContains(self.response, self.client1.email)


class DeleteViewTest(TestBase):

	def setUp(self):
		self.login()
		self.client1 = create_client(commit=True)
		self.client2 = create_client(commit=True, name='Andre', email='a@email.com')

		# Creating data to client 1
		self.item1 = create_item(client=self.client1, commit=True)
		self.picture1 = create_picture(self.item1)
		self.picture2 = create_picture(self.item1)

		# Creating data to client 2
		self.item2 = create_item(client=self.client2, commit=True)
		self.picture3 = create_picture(self.item2)
		self.picture4 = create_picture(self.item2)

		# Before post must have: 
		# 2 clients,
		# 2 items
		# 4 pictures
		self.assertEqual(len(ModelClient.objects.all()), 2)
		self.assertEqual(len(Item.objects.all()), 2)
		self.assertEqual(len(Picture.objects.all()), 4)

		self.response = self.client.post(reverse('client:delete', args=[self.client1.pk]), follow=True)	

	def test_redirected(self):
		expected_url = reverse('client:list')
		
		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)

	def test_if_deleted(self):
		"""
			After post, must have be deleted the client
			and the itens/pictures bonded with him.

			Must have: 
			1 client,
			1 item,
			2 pictures.
		"""
		self.assertEqual(len(ModelClient.objects.all()), 1)
		self.assertEqual(len(Item.objects.all()), 1)
		self.assertEqual(len(Picture.objects.all()), 2)		

	def test_message(self):
		self.assertContains(self.response, 'Cliente removido com sucesso!')


class ListItemsViewTest(TestBase):
	
	def setUp(self):
		self.login()
		self.client1 = create_client(commit=True)

		#creating items to the client
		self.item1 = create_item(client=self.client1, commit=True)
		self.item2 = create_item(client=self.client1, commit=True,
		 name='Chair')
		self.item3 =  create_item(client=self.client1, commit=True,
		 name='Table')
		
		self.url = reverse('client:list_items', args=[self.client1.pk])
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_get_logout(self):
		self._test_get_logout(self.url)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'client/list_items.html')

	def test_context(self):
		items = self.response.context['items']
		self.assertIsInstance(items, QuerySet)
		
		amount = self.response.context['amount']
		self.assertEqual(amount, 3)

		total = self.response.context['total']
		self.assertEqual(total, 3000,00)

		received = self.response.context['received']
		self.assertEqual(received, 1500,00)

		owing = self.response.context['owing']
		self.assertTrue(owing)

	def test_html(self):
		self.assertContains(self.response, self.client1.name)
		self.assertContains(self.response, self.item1.name)
		self.assertContains(self.response, self.item2.name)
		self.assertContains(self.response, self.item3.name)

	def test_when_is_empty(self):
		Item.objects.all().delete()
		
		self.response = self.client.get(self.url)
		
		expected = 'Nenhum item cadastrado para {}'.format(self.client1.name) 
		self.assertContains(self.response, expected)
	