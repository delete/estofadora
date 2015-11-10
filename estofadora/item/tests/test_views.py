import os

from django.core.urlresolvers import reverse

from estofadora.client.tests import create_client

from . import (
	TestBase, ItemForm, create_item, Item, make_validated_form,
	PictureFormSet, make_managementform_data, PATH_TO_IMAGE_TEST,
	Picture, create_picture
) 


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

	def test_if_has_forms(self):
		item_form = self.response.context['item_form']
		picture_formset = self.response.context['picture_formset']
		
		self.assertIsInstance(item_form, ItemForm)
		self.assertIsInstance(picture_formset, PictureFormSet)

	def test_html(self):
		self.assertContains(self.response, '<form')
		self.assertContains(self.response, '<input', 14)
		self.assertContains(self.response, 'type="submit"')

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')


class AddPostWithoutImageTest(TestBase):
	"""
		Test post without images.
	"""
	def setUp(self):
		self.login()
		data = make_validated_form(commit=False)
		data.update(make_managementform_data())
		self.response = self.client.post(reverse('item:add'), data)

	def test_message(self):
		self.assertContains(self.response, 'Item cadastrado com sucesso!')

	def test_if_saved(self):
		self.assertTrue(Item.objects.exists())


class AddPostWithImageTest(TestBase):
	"""
		Test post with image.
	"""
	def setUp(self):
		self.login()
		data = make_validated_form(commit=False)
		
		with open(PATH_TO_IMAGE_TEST, 'rb') as img:
			data_new = {
				'pictures-0-image': img,
			}
			data.update(make_managementform_data(**data_new))

			self.response = self.client.post(reverse('item:add'), data)

	def test_message(self):
		self.assertContains(self.response, 'Item cadastrado com sucesso!')

	def test_if_saved(self):
		self.assertEqual(len(Item.objects.all()), 1)
		self.assertEqual(len(Picture.objects.all()), 1)


class AddInvalidItemPostTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('item:add')

	def test_post_name_is_required(self):
		data = make_validated_form(name='', commit=False)
		self._test_if_got_errors(data)

	def test_post_description_is_required(self):
		data = make_validated_form(description='', commit=False)
		self._test_if_got_errors(data)

	def test_post_delivery_date_is_required(self):
		data = make_validated_form(delivery_date='', commit=False)
		self._test_if_got_errors(data)

	def test_post_wrong_delivery_date(self):
		data = make_validated_form(delivery_date='2015/01/21 22:00:00',
									commit=False)
		self._test_if_got_errors(data)

	def _test_if_got_errors(self, data):
		data.update(make_managementform_data())
		self.response = self.client.post(self.url, data)
		self.assertTrue(self.response.context['item_form'].errors)
		self.assertTrue(self.response.context['picture_formset'].errors)


class AddInvalidImagePostTest(TestBase):

	def setUp(self):
		self.login()
		self.url = reverse('item:add')

	def test_post_image_wrong_value(self):
		data = make_validated_form(commit=False)
		data_new = {'pictures-0-image': 'error'}
		data.update(make_managementform_data(**data_new))
		self._test_if_got_errors(data)

	def _test_if_got_errors(self, data):
		self.response = self.client.post(self.url, data)
		self.assertFalse(self.response.context['item_form'].errors)
		self.assertTrue(self.response.context['picture_formset'].errors)


class EditViewTest(AddViewTest):

	def setUp(self):
		self.login()
		self.item = create_item(commit=True)
		self.url = reverse('item:edit', args=[self.item.pk])
		self.response = self.client.get(self.url)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'item/edit.html')

	def test_if_has_forms(self):
		form = self.response.context['form']

		self.assertIsInstance(form, ItemForm)

	def test_html(self):
		self.assertContains(self.response, '<form')
		self.assertContains(self.response, '<input', 6)
		self.assertContains(self.response, 'type="submit"')


class EditPostTest(TestBase):
	
	def setUp(self):
		self.login()
		self.item = create_item(commit=True)
		self.url = reverse('item:edit', args=[self.item.pk])
		self.response = self.client.get(self.url)

		self.form = self.response.context['form']
		self.data = self.form.initial		

	def test_post_name(self):
		self.data['name'] = 'Chair'
		
		self._post_and_test_response()
		self.assertEqual(Item.objects.first().name, 'Chair')

	def test_post_description(self):
		self.data['description'] = 'For sale!'
		
		self._post_and_test_response()
		self.assertEqual(Item.objects.first().description, 'For sale!')

	def test_post_concluded(self):
		self.data['concluded'] = True
		
		self._post_and_test_response()
		self.assertEqual(Item.objects.first().concluded, True)

	def test_post_total_value(self):
		self.data['total_value'] = 2000
		
		self._post_and_test_response()
		self.assertEqual(Item.objects.first().total_value, 2000)

	def test_post_total_paid(self):
		self.data['total_paid'] = 1000
		
		self._post_and_test_response()
		self.assertEqual(Item.objects.first().total_paid, 1000)

	def test_post_delivery_date(self):
		self.data['delivery_date'] = '19/01/2020 22:00:00'
		
		self._post_and_test_response()
		
		expected_date = '19/01/2020 22:00:00'
		saved_date = Item.objects.first().delivery_date.strftime("%d/%m/%Y %H:%M:%S")
		
		self.assertEqual(saved_date, expected_date)

	def _post_and_test_response(self):
		
		self.response = self.client.post(self.url, self.data)
		self.assertContains(self.response, 'Item alterado com sucesso!')


class EditInvalidPostTest(TestBase):

	def setUp(self):
		self.login()
		self.item = create_item(commit=True)
		self.url = reverse('item:edit', args=[self.item.pk])
		self.response = self.client.get(self.url)

		self.form = self.response.context['form']
		self.data = self.form.initial	

	def test_post_name_required(self):
		self.data['name'] = ''
		
		self._test_if_got_errors()

	def test_post_description_required(self):
		self.data['description'] = ''
		
		self._test_if_got_errors()

	def test_post_delivery_date_required(self):
		self.data['delivery_date'] = ''
		
		self._test_if_got_errors()	

	def _test_if_got_errors(self):
		self.response = self.client.post(self.url, self.data)
		self.assertTrue(self.response.context['form'].errors)


class ListViewTest(TestBase):

	def setUp(self):
		self.login()
		self.item1 = create_item(commit=True)

		self.client2 = create_client(commit=True, name='Andre', email='a@email.com')
		self.item2 = create_item(client=self.client2, commit=True, name='Box')
		self.item3 = create_item(client=self.client2, commit=True, name='Chair')
		self.item4 = create_item(client=self.client2, commit=True, name='Table')

		self.response = self.client.get(reverse('item:list'))

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'item/list.html')

	def test_if_contains_items(self):
		self.assertContains(self.response, self.item1.name)
		self.assertContains(self.response, self.item1.client.name)
		self.assertContains(self.response, self.item2.name)
		self.assertContains(self.response, self.item2.client.name)

	def test_if_contains_search_field(self):
		self.assertContains(self.response, '<form')
		self.assertContains(self.response, 'type="submit"')

	def test_post(self):
		data = {'name':'Andre'}
		self.response = self.client.post(reverse('item:list'), data)
		self.assertContains(self.response, self.client2.name)
		self.assertContains(self.response, self.item2.name)
		self.assertContains(self.response, self.item3.name)
		self.assertContains(self.response, self.item4.name)

		#client1 items should not appear
		self.assertNotContains(self.response, self.item1.client.name)
		self.assertNotContains(self.response, self.item1.name)

	def test_massage_when_view_is_empty(self):
		Item.objects.all().delete()
		self.response = self.client.get(reverse('item:list'))
		self.assertContains(self.response, 'Nenhum item cadastrado!')


class DeleteViewTest(TestBase):

	def setUp(self):
		self.login()
		self.item1 = create_item(commit=True)

		self.client2 = create_client(commit=True, name='Andre', email='a@email.com')
		self.item2 = create_item(client=self.client2, commit=True)

		self.assertEqual(len(Item.objects.all()), 2)
		
		self.response = self.client.post(reverse('item:delete', args=[self.item2.pk]), follow=True)
	
	def test_redirect(self):
		expected_url = reverse('item:list')

		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)

	def test_if_deleted(self):
		self.assertEqual(len(Item.objects.all()), 1)

	def test_message(self):
		self.assertContains(self.response, 'Item removido com sucesso!')


class ImageListViewTest(TestBase):

	def setUp(self):
		self.login()
		self.item1 = create_item(commit=True)
		self.picture = create_picture(self.item1)

		self.url = reverse('item:image_list', args=[self.item1.pk])
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

	def test_get_logout(self):
		self._test_get_logout(self.url)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'item/list_images.html')

	def test_if_contains_items(self):
		self.assertContains(self.response, self.item1.name)
		self.assertContains(self.response, self.item1.client.name)			
		self.assertContains(self.response, self.picture.image.url)

	def test_massage_when_view_is_empty(self):
		Picture.objects.all().delete()
		self.response = self.client.get(self.url)
		self.assertContains(self.response, 'Nenhuma imagem adicionada!')	

	def test_if_has_forms(self):
		picture_formset = self.response.context['picture_formset']
		
		self.assertIsInstance(picture_formset, PictureFormSet)


class ImageListViewPostWithImageTest(TestBase):
	"""
		Test post with image.
	"""

	def setUp(self):
		self.login()
		self.item1 = create_item(commit=True)

		self.url = reverse('item:image_list', args=[self.item1.pk])
		
		with open(PATH_TO_IMAGE_TEST, 'rb') as img:
			data_new = {
				'pictures-0-image': img,
			}
			data = make_managementform_data(**data_new)

			self.response = self.client.post(self.url, data, follow=True)

	def test_message(self):
		self.assertContains(self.response, 'Imagem enviada com sucesso!')

	def test_redirect(self):
		expected_url = reverse('item:image_list', args=[self.item1.pk])

		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)

	def test_if_saved(self):
		self.assertTrue(Picture.objects.exists())


class ImageDeleteViewTest(TestBase):

	def setUp(self):
		self.login()
		self.item1 = create_item(commit=True)

		self.picture1 = create_picture(self.item1)
		self.picture2 = create_picture(self.item1)

		self.assertEqual(len(Picture.objects.all()), 2)
		
		self.response = self.client.post(reverse('item:image_delete', args=[self.picture1.pk]), follow=True)
	
	def test_redirect(self):
		expected_url = reverse('item:image_list', args=[self.item1.pk])

		self.assertRedirects(self.response, expected_url, status_code=302, target_status_code=200)

	def test_if_deleted(self):
		self.assertEqual(len(Picture.objects.all()), 1)

	def test_if_image_file_was_deleted(self):
		path = self.picture1.image.path
		self.assertFalse(os.path.exists(path))

	def test_message(self):
		self.assertContains(self.response, 'Imagem removida com sucesso!')