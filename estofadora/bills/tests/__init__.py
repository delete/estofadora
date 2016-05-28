from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

from estofadora.statement.models import Cash
from estofadora.bills.models import Bill
from estofadora.bills.forms import BillForm


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
        User.objects.all().delete()
        Cash.objects.all().delete()
        Bill.objects.all().delete()

    def _test_get_logout(self, url):
        self.logout()
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 302)


def make_validated_form(commit=True, **kwargs):
    data = {
        'date_to_pay': '2015-10-17',
        'name': 'Client',
        'value': 0,
        'is_paid': False
    }
    data.update(kwargs)
    if commit:
        form = BillForm(data)
        form.is_valid()
        return form
    else:
        return data


def create_bill(commit=True, **kwargs):
    data = {
        'date_to_pay': '2015-10-17',
        'name': 'Client',
        'value': 0,
        'is_paid': False
    }
    data.update(kwargs)
    if commit:
        return Bill.objects.create(**data)

    return data
