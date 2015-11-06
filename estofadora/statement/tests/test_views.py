#conding: utf-8
import datetime

from django.core.urlresolvers import reverse

from . import TestBase, CashForm, Cash, make_validated_form, create_cash


class HomeViewTest(TestBase):

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
		self.assertContains(self.response, 'Caixa diário')


class CashViewTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('statement:cash')
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):		
		self.assertTemplateUsed(self.response, 'statement/cash.html')
	
	def test_get_logout(self):
		self._test_get_logout(self.url)

	def test_if_has_form(self):
		form = self.response.context['form']
		self.assertIsInstance(form, CashForm)

	def test_html(self):
		# + csrf input
		self.assertContains(self.response, '<input', 7)
		self.assertContains(self.response, 'submit', 2)

	def test_data_after_post(self):
		today = datetime.datetime.now().date()
		cash = create_cash(commit=True, date=today)

		self.response = self.client.get(self.url)

		self.assertContains(self.response, cash.history)
		self.assertContains(self.response, cash.expenses)
		self.assertContains(self.response, cash.income)
		self.assertContains(self.response, cash.total)


class CashSavePostTest(TestBase):

	def setUp(self):
		self.login()
		data = make_validated_form(commit=False)
		self.response = self.client.post(reverse('statement:cash'), data, follow=True)

	def test_message(self):
		self.assertContains(self.response, 'Registrado com sucesso!')

	def test_if_saved(self):
		self.assertTrue(Cash.objects.exists())

	def test_redirected(self):
		expected_url = reverse('statement:cash')
		
		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)


class CashInvalidPostTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('statement:cash')

	def test_post_date_required(self):
		data = make_validated_form(date='', commit=False)
		self._test_if_got_errors(data)

	def test_post_history_required(self):
		data = make_validated_form(history='', commit=False)
		self._test_if_got_errors(data)
	
	def test_post_income_required(self):
		data = make_validated_form(income='', commit=False)
		self._test_if_got_errors(data)

	def test_post_expenses_required(self):
		data = make_validated_form(expenses='', commit=False)
		self._test_if_got_errors(data)

	def _test_if_got_errors(self, data):
		self.response = self.client.post(self.url, data)
		self.assertTrue(self.response.context['form'].errors)


class CashSearchPostTest(TestBase):
	#TODO
	pass


class DeleteViewTest(TestBase):

	def setUp(self):
		self.login()
		
		self.cash1 = create_cash(commit=True)
		self.cash2 = create_cash(commit=True)
		
		self.response = self.client.post(reverse('statement:delete', args=[self.cash1.pk]), follow=True)

	def test_redirected(self):
		expected_url = reverse('statement:cash')
		
		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)

	def test_if_deleted(self):
		self.assertEqual(len(Cash.objects.all()), 1)

	def test_message(self):
		self.assertContains(self.response, 'Registro removido com sucesso!')


class EditViewTest(TestBase):

	def setUp(self):
		self.login()
		self.cash = create_cash(commit=True)
		self.url = reverse('statement:edit', args=[self.cash.pk])
		self.response = self.client.get(self.url)

	def tearDown(self):
		Cash.objects.all().delete()
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_get_logout(self):
		self._test_get_logout(self.url)

	def test_if_has_form(self):
		form = self.response.context['form']
		self.assertIsInstance(form, CashForm)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_template(self):
		self.assertTemplateUsed(self.response, 'statement/item_edit_form.html')


class EditPostTest(TestBase):

	def setUp(self):
		self.login()
		self.cash = create_cash(commit=True)
		self.url = reverse('statement:edit', args=[self.cash.pk])
		self.response = self.client.get(self.url)

		self.form = self.response.context['form']
		self.data = self.form.initial

	def test_message(self):
		self.response = self.client.post(self.url, self.data)
		self.assertContains(self.response, 'Item alterado com sucesso!')

	def test_post_income(self):
		'Test if income has change'
		self.data['income'] = '200'

		self.response = self.client.post(self.url, self.data)
		self.assertEqual(Cash.objects.first().income, 200.00)

	def test_post_expenses(self):
		'Test if expenses has change'
		self.data['expenses'] = '120'

		self.response = self.client.post(self.url, self.data)
		self.assertEqual(Cash.objects.first().expenses, 120.00)

	def test_post_history(self):
		'Test if history has change'
		self.data['history'] = 'Bill to pay'
		
		self.response = self.client.post(self.url, self.data)
		self.assertEqual(Cash.objects.first().history, 'Bill to pay')

	def test_post_date(self):
		'Test if history has change'
		self.data['date'] = '2015-10-10'
		
		self.response = self.client.post(self.url, self.data)
		self.assertEqual(Cash.objects.first().date.isoformat(), '2015-10-10')

	def test_post_date_two(self):
		self.data['date'] = '10/10/2015'
		
		self.response = self.client.post(self.url, self.data)
		self.assertEqual(Cash.objects.first().date.isoformat(), '2015-10-10')

	def test_if_total_has_change(self):
		'Test if total has change and is right'
		self.data['income'] = '200'
		self.data['expenses'] = '100'
		
		self.response = self.client.post(self.url, self.data)
		self.assertEqual(Cash.objects.first().total, 100.00)


class EditInvalidPostTest(TestBase):

	def setUp(self):
		self.login()
		self.cash = create_cash(commit=True)
		self.url = reverse('statement:edit', args=[self.cash.pk])
		self.response = self.client.get(self.url)

		self.form = self.response.context['form']
		self.data = self.form.initial	

	def test_post_date_required(self):
		self.data['date'] = ''

		self._test_if_got_errors()

	def test_post_wrong_date(self):
		self.data['date'] = '10-10-2015'

		self._test_if_got_errors()

	def test_post_income_required(self):
		self.data['income'] = ''
		
		self._test_if_got_errors()

	def test_post_expenses_required(self):
		self.data['expenses'] = ''
		
		self._test_if_got_errors()

	def test_post_history_required(self):
		self.data['history'] = ''
		
		self._test_if_got_errors()

	def _test_if_got_errors(self):
		self.response = self.client.post(self.url, self.data)
		self.assertTrue(self.response.context['form'].errors)
		self.assertTrue(self.response.context['form_error'])


class CashMonthViewTest(TestBase):

	def setUp(self):
		self.login()

		self.today = datetime.datetime.now().date()
		self.url = reverse('statement:cash_month')
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):		
		self.assertTemplateUsed(self.response, 'statement/cash_month.html')
	
	def test_get_logout(self):
		self._test_get_logout(self.url)

	def test_html(self):
		# + csrf input
		self.assertContains(self.response, '<input', 1)
		self.assertContains(self.response, 'submit', 1)
		self.assertContains(self.response, '<select', 2)

	def test_message_when_is_empty(self):
		'Must return a warning message when there are not any registry'
		self.assertContains(self.response, 'Nenhum registro encontrado na data:')

	def test_date_in_context(self):
		'When was not choose a specific date, the default date is "today"'
		self.assertEqual(self.response.context['choose_date'], self.today)


class CashMonthSeachPostTest(TestBase):

	def setUp(self):
		self.login()
		
		september = datetime.datetime(2015, 9, 10)

		october = datetime.datetime(2015, 10, 10)

		self.cash1 = create_cash(
			commit=True, history='Cash1', date=september.date(),
			expenses=100, income=100
		)
		self.cash2 = create_cash(
			commit=True, history='Cash2', date=september.date(),
			expenses=200, income=200
		)
		self.cash3 = create_cash(
			commit=True, history='Cash3', date=october.date(),
			expenses=300, income=300
		)

		data = {
			'selectmonth': september.date().month,
			'selectyear': september.date().year
		}

		self.response = self.client.post(reverse('statement:cash_month'), data,
			follow=True)

	def test_data_after_post(self):
		'The response must have the data of cash1 and cash2, only'
		self.assertContains(self.response, self.cash1.history)
		self.assertContains(self.response, self.cash1.income)
		self.assertContains(self.response, self.cash1.expenses)

		self.assertContains(self.response, self.cash2.history)
		self.assertContains(self.response, self.cash2.income)
		self.assertContains(self.response, self.cash2.expenses)		

		self.assertNotContains(self.response, self.cash3.history)
		self.assertNotContains(self.response, self.cash3.income)
		self.assertNotContains(self.response, self.cash3.expenses)

	def test_in_another_date(self):
		'If there are not registries, must return a warning message'
		
		data = {
			'selectmonth': '01',
			'selectyear': '2014'
		}

		self.response = self.client.post(reverse('statement:cash_month'), data,
			follow=True)

		self.assertContains(self.response, 'Nenhum registro encontrado na data:')
