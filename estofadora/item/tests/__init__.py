#conding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile

from estofadora.settings import BASE_DIR, PATH_TO_IMAGE_TEST
from estofadora.item.forms import ItemForm, PictureFormSet, ItemPictureForm
from estofadora.item.models import Item, Picture
from estofadora.client.models import Client as ModelClient
from estofadora.client.tests import create_client


class TestBase(TestCase):

	def _create_user(self):
		user = User.objects.create_user('admin', 'a@a.com', '123')
		return user

	def login(self, username='admin', password='123'):
		self._create_user()
		self.client = Client()
		self.client.login(username=username, password=password)
	
	def logout(self):
		self.client.logout()

	def tearDown(self):
		self.logout()
		Item.objects.all().delete()
		ModelClient.objects.all().delete()
		User.objects.all().delete()
		Picture.objects.all().delete()

	def _test_get_logout(self, url):
		self.logout()
		self.response = self.client.get(url)
		self.assertEqual(self.response.status_code, 302)


def create_item(commit=False, client=None, **kwargs):
	if not client:
		client = create_client(commit=True)

	data = {
		'client': client,
		'name': 'Sofa',
		'description': 'Was bad, but now, is good.',
		'delivery_date': '2016-01-17 22:40',
		'total_value': 1000,
		'total_paid': 500,
	}
	data.update(kwargs)	
	if commit:
		return Item.objects.create(**data)
	
	return data


def make_validated_item_form(client=None, commit=True, **kwargs):
	if not client:
		client = create_client(commit=True)
	data = {
		'client': client.pk,
		'name': 'Sofa',
		'description': 'Was bad, but now, is good.',		
		'delivery_date': '2016-01-17 22:40',
		'total_value': '1000',
		'total_paid': '500',
	}
	data.update(kwargs)
	if commit:
		form = ItemForm(data)
		form.is_valid()
		return form
	else:
		return data


def make_validated_item_picture_form(client=None, commit=True, **kwargs):
	if not client:
		client = create_client(commit=True)
	data = {
		'client': client.pk,
		'name': 'Sofa',
		'description': 'Was bad, but now, is good.',		
		'delivery_date': '2016-01-17 22:40',
		'total_value': '1000',
		'total_paid': '500',
		'files': ''
	}
	data.update(kwargs)
	if commit:
		form = ItemPictureForm(data)
		form.is_valid()
		return form
	else:
		return data


def create_picture(item, **kwargs):
	image_file = SimpleUploadedFile(
		'test.png',
		open(PATH_TO_IMAGE_TEST, 'rb').read()
	)
	data = {
		'item': item,
		'image': image_file,
		'state': 'before',
		'public': False 
	}
	data.update(kwargs)
	picture = Picture.objects.create(**data)
	return picture


def make_managementform_data(**kwargs):
	data={
		'pictures-TOTAL_FORMS': 3,
		'pictures-INITIAL_FORMS': 0,
		'pictures-MAX_NUM_FORMS': 1000,
		'pictures-0-image': '',
		'pictures-1-image': '',
		'pictures-2-image': '',
	}
	data.update(kwargs)
	return data