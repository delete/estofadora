# coding: utf-8
import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client


from estofadora.core.forms import ContactForm

from estofadora.core.models import Contact
from estofadora.item.models import Item, Picture
from estofadora.client.models import Client as ModelClient
from estofadora.bills.models import Bill

from estofadora.item.tests import create_item, create_picture, create_client
from estofadora.bills.tests import create_bill


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
        Bill.objects.all().delete()

    def _test_get_logout(self, url):
        self.logout()
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 302)


def make_validated_form(commit=True, **kwargs):
    data = {
        'name': 'MyName',
        'email': 'myemai@email.com',
        'telephone': '11111111',
        'subject': 'About',
        'description': 'Was bad, but now, is good.',
    }
    data.update(kwargs)
    if commit:
        form = ContactForm(data)
        form.is_valid()
        return form
    else:
        return data


def create_contact(commit=False, **kwargs):
    data = {
        'name': 'MyName',
        'email': 'myemai@email.com',
        'telephone': '11111111',
        'subject': 'About',
        'description': 'Was bad, but now, is good.',
    }
    data.update(kwargs)
    if commit:
        return Contact.objects.create(**data)

    return data
