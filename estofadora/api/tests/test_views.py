from . import (
	TestBase, create_client, create_bill, create_item, ModelClient,
	Bill, Item
)


class ClientsGetResponseTest(TestBase):
	"""
		Test GET in /api/clients/
	"""
	def setUp(self):
		self.login()

		self.url = '/api/clients/'

	def test_logout(self):
		self.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.data, {'detail': 'As credenciais de autenticação não foram fornecidas.'})

	def test_empty(self):
		response = self.client.get(self.url)
		self.assertEqual(response.data.get('count'), 0)

	def test_with_1_client(self):
		create_client(commit=True)

		response = self.client.get(self.url)
		self.assertEqual(response.data.get('count'), 1)


class OneClientGetResponseTest(TestBase):
	"""
		Test GET in /api/clients/:id/
	"""
	def setUp(self):
		self.login()

		self.url = '/api/clients/{}/'

	def test_logout(self):
		self.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.data, {'detail': 'As credenciais de autenticação não foram fornecidas.'})

	def test_with_wrong_id(self):
		response = self.client.get(self.url.format(22))
		self.assertEqual(response.data.get('detail'), 'Não encontrado.')

	def test_with_right_id(self):
		client = create_client(commit=True)

		response = self.client.get(self.url.format(client.pk))
		self.assertEqual(response.data.get('name'), client.name)
		self.assertEqual(response.data.get('email'), client.email)


class ClientPostTest(TestBase):
	"""
		Test POST in /api/clients/
	"""
	def setUp(self):
		self.login()

		self.url = '/api/clients/'

		#Before post, there is not client yet.
		self.assertFalse(ModelClient.objects.exists())

		data = create_client()

		response = self.client.post(self.url, data, format='json')

	def test_if_saved(self):
		self.assertTrue(ModelClient.objects.exists())


class ClientPutTest(TestBase):
	"""
		Test PUT in /api/clients/:id/
	"""
	def setUp(self):
		self.login()

		self.client1 = create_client(commit=True)

		self.url = '/api/clients/{}/'.format(self.client1.pk)

		#Before post, name must be just 'Fellipe'
		self.assertEqual(self.client1.name, 'Fellipe')

		self.new_name = 'Fellipe Pinheiro'
		
		data = create_client()
		data['name'] = self.new_name

		response = self.client.put(self.url, data, format='json')

	def test_if_changed(self):
		client = ModelClient.objects.get(pk=self.client1.pk)

		self.assertEqual(client.name, self.new_name)


class BillsGetResponseTest(TestBase):
	"""
		Test GET in /api/bills/
	"""
	def setUp(self):
		self.login()

		self.url = '/api/bills/'

	def test_logout(self):
		self.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.data, {'detail': 'As credenciais de autenticação não foram fornecidas.'})

	def test_empty(self):
		response = self.client.get(self.url)
		self.assertEqual(response.data.get('count'), 0)

	def test_with_1_bill(self):
		bill = create_bill(commit=True)

		response = self.client.get(self.url)
		self.assertEqual(response.data.get('count'), 1)


class OneBillGetResponseTest(TestBase):
	"""
		Test GET in /api/bills/:id/
	"""
	def setUp(self):
		self.login()

		self.url = '/api/bills/{}/'

	def test_logout(self):
		self.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.data, {'detail': 'As credenciais de autenticação não foram fornecidas.'})

	def test_with_wrong_id(self):
		response = self.client.get(self.url.format(22))
		self.assertEqual(response.data.get('detail'), 'Não encontrado.')

	def test_with_right_id(self):
		bill = create_bill(commit=True)

		response = self.client.get(self.url.format(bill.pk))
		self.assertEqual(response.data.get('name'), bill.name)
		self.assertEqual(response.data.get('date_to_pay'), bill.date_to_pay)


class BillPostTest(TestBase):
	"""
		Test POST in /api/bills/
	"""
	def setUp(self):
		self.login()

		self.url = '/api/bills/'

		#Before post, there is not bill yet.
		self.assertFalse(Bill.objects.exists())

		data = create_bill()

		response = self.client.post(self.url, data, format='json')

	def test_if_saved(self):
		self.assertTrue(Bill.objects.exists())


class BillPutTest(TestBase):
	"""
		Test PUT in /api/bills/:id/
	"""
	def setUp(self):
		self.login()

		self.bill = create_bill(commit=True)

		self.url = '/api/bills/{}/'.format(self.bill.pk)

		#Before post, name must be just 'Client'
		self.assertEqual(self.bill.name, 'Client')

		self.new_name = 'Light'
		
		data = create_bill()
		data['name'] = self.new_name

		response = self.client.put(self.url, data, format='json')

	def test_if_changed(self):
		bill = Bill.objects.get(pk=self.bill.pk)

		self.assertEqual(bill.name, self.new_name)



class ItemsGetResponseTest(TestBase):
	"""
		Test GET in /api/items/
	"""
	def setUp(self):
		self.login()

		self.url = '/api/items/'

	def test_logout(self):
		self.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.data, {'detail': 'As credenciais de autenticação não foram fornecidas.'})

	def test_empty(self):
		response = self.client.get(self.url)
		self.assertEqual(response.data.get('count'), 0)

	def test_with_1_item(self):
		client = create_client(commit=True)
		create_item(client=client, commit=True)

		response = self.client.get(self.url)
		self.assertEqual(response.data.get('count'), 1)


class OneItemGetResponseTest(TestBase):
	"""
		Test GET in /api/items/:id/
	"""
	def setUp(self):
		self.login()

		self.url = '/api/items/{}/'

	def test_logout(self):
		self.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.data, {'detail': 'As credenciais de autenticação não foram fornecidas.'})

	def test_with_wrong_id(self):
		response = self.client.get(self.url.format(22))
		self.assertEqual(response.data.get('detail'), 'Não encontrado.')

	def test_with_right_id(self):
		client = create_client(commit=True)
		item = create_item(client=client, commit=True)

		response = self.client.get(self.url.format(item.pk))
		self.assertEqual(response.data.get('name'), item.name)
		self.assertEqual(response.data.get('client'), item.client.pk)


class ItemPostTest(TestBase):
	"""
		Test POST in /api/items/
	"""
	def setUp(self):
		self.login()

		self.url = '/api/items/'

		#Before post, there is not item yet.
		self.assertFalse(Item.objects.exists())

		client = create_client(commit=True)
		data = create_item(client=client.pk)

		response = self.client.post(self.url, data, format='json')

	def test_if_saved(self):
		self.assertTrue(Item.objects.exists())


class ItemPutTest(TestBase):
	"""
		Test PUT in /api/items/:id/
	"""
	def setUp(self):
		self.login()

		self.item = create_item(commit=True)

		self.url = '/api/items/{}/'.format(self.item.pk)

		#Before post, name must be just 'Sofa'
		self.assertEqual(self.item.name, 'Sofa')

		self.new_name = 'Table'
		
		data = create_item(client=self.item.client.pk)
		data['name'] = self.new_name

		response = self.client.put(self.url, data, format='json')

	def test_if_changed(self):
		item = Item.objects.get(pk=self.item.pk)

		self.assertEqual(item.name, self.new_name)