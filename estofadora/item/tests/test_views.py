from django.core.urlresolvers import reverse

from . import TestBase, ItemForm, create_item, Item, make_validated_form


class AddViewTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('item:add')
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_get_logout(self):
		self._test_get_logout(self.url)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'item/add.html')

	def test_if_has_form(self):
		form = self.response.context['form']
		self.assertIsInstance(form, ItemForm)

	def test_html(self):
		self.assertContains(self.response, '<form')
		self.assertContains(self.response, '<input', 6)
		self.assertContains(self.response, '<input', 6)
		self.assertContains(self.response, 'type="submit"')

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')


class AddPostTest(TestBase):

	def setUp(self):
		self.login()
		data = make_validated_form(commit=False)
		self.response = self.client.post(reverse('item:add'), data)

	def test_message(self):
		self.assertContains(self.response, 'Item cadastrado com sucesso!')

	def test_if_saved(self):
		self.assertTrue(Item.objects.exists())


class AddInvalidPostTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('client:add')

	def test_post_name_required(self):
		data = make_validated_form(name='', commit=False)
		self._test_if_got_errors(data)

	def test_post_description_required(self):
		data = make_validated_form(description='', commit=False)
		self._test_if_got_errors(data)

	def test_post_delivery_date_required(self):
		data = make_validated_form(delivery_date='', commit=False)
		self._test_if_got_errors(data)

	def test_post_fail_delivery_date(self):
		data = make_validated_form(delivery_date='2015/01/21 22:00', commit=False)
		self._test_if_got_errors(data)

	def _test_if_got_errors(self, data):
		self.response = self.client.post(self.url, data)
		self.assertTrue(self.response.context['form'].errors)