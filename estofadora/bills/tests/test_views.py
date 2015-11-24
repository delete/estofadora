#conding: utf-8
import datetime

from django.core.urlresolvers import reverse

from . import TestBase, Bill, create_bill, BillForm, make_validated_form, Cash


class NewViewTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('bills:new')
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):		
		self.assertTemplateUsed(self.response, 'bills/new.html')
	
	def test_get_logout(self):
		self._test_get_logout(self.url)

	def test_html(self):
		# + csrf input
		self.assertContains(self.response, '<input', 4)
		self.assertContains(self.response, 'submit', 1)
	
	def test_if_has_form(self):
		form = self.response.context['form']
		self.assertIsInstance(form, BillForm)


class NewSavePostTest(TestBase):

	def setUp(self):
		self.login()
		data = make_validated_form(commit=False)
		self.response = self.client.post(reverse('bills:new'), data,
			follow=True)

	def test_message(self):
		self.assertContains(self.response, 'Cadastrada com sucesso!')

	def test_if_saved(self):
		self.assertTrue(Bill.objects.exists())

	def test_if_cash_has_saved(self):
		'Must save a Cash object too'
		self.assertTrue(Cash.objects.exists())


class ListViewTest(TestBase):

	def setUp(self):
		self.login()

		self.bill1 = create_bill(is_paid=True, commit=True)
		self.bill2 = create_bill(name='Client2', commit=True)

		self.url = reverse('bills:list')
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):		
		self.assertTemplateUsed(self.response, 'bills/list.html')
	
	def test_get_logout(self):
		self._test_get_logout(self.url)

	def test_html(self):
		self.assertContains(self.response, self.bill1.name)
		self.assertContains(self.response, self.bill1.value)
		# The bill1 was paid.
		self.assertContains(self.response, 'Pago', 1)

		self.assertContains(self.response, self.bill2.name)
		self.assertContains(self.response, self.bill2.value)

	def test_empty(self):
		Bill.objects.all().delete()

		self.response = self.client.get(self.url)
		self.assertContains(self.response, 'Nenhuma conta cadastrada.')
