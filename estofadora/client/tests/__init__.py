# conding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

from estofadora.client.forms import ClientForm
from estofadora.client.models import Client as ModelClient


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
        ModelClient.objects.all().delete()
        User.objects.all().delete()

    def _test_get_logout(self, url):
        self.logout()
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 302)


def create_client(commit=True, **kwargs):
    data = {
        'name': 'Fellipe',
        'email': 'email@email.com',
        'adress': 'Street',
        'telephone1': '123',
        'telephone2': '321',
    }
    data.update(kwargs)
    if commit:
        return ModelClient.objects.create(**data)

    return data


def make_validated_form(**kwargs):
    data = {
        'name': 'Fellipe',
        'email': 'email@email.com',
        'adress': 'Street',
        'telephone1': '123',
        'telephone2': '321',
    }
    data.update(kwargs)
    form = ClientForm(data)
    form.is_valid()
    return form
