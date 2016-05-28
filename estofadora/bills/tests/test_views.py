# conding: utf-8
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
        self.response = self.client.post(
            reverse('bills:new'), data, follow=True
        )

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

        self.bill1 = create_bill(is_paid=True)
        self.bill2 = create_bill(name='Client2')

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


class DeleteViewTest(TestBase):

    def setUp(self):
        self.login()

        self.bill1 = create_bill(is_paid=True)
        self.bill2 = create_bill(name='Client2')

        # Must have 2 bills before post.
        self.assertEqual(len(Bill.objects.all()), 2)

        self.response = self.client.post(
            reverse('bills:delete', args=[self.bill2.pk]), follow=True
        )

    def test_redirect(self):
        expected_url = reverse('bills:list')

        self.assertRedirects(
            self.response, expected_url,
            status_code=302, target_status_code=200
        )

    def test_if_deleted(self):
        self.assertEqual(len(Bill.objects.all()), 1)

    def test_message(self):
        self.assertContains(self.response, 'Conta removida com sucesso!')


class MarkAsPaidViewTest(TestBase):

    def setUp(self):
        self.login()

        self.bill1 = create_bill()

        # Must be False before post
        self.assertFalse(self.bill1.is_paid)

        self.response = self.client.post(
            reverse('bills:mark_as_paid', args=[self.bill1.pk]), follow=True
        )

    def test_redirect(self):
        expected_url = reverse('bills:list')

        self.assertRedirects(
            self.response, expected_url,
            status_code=302, target_status_code=200
        )

    def test_if_changes(self):
        bill = Bill.objects.get(pk=self.bill1.pk)
        self.assertTrue(bill.is_paid)

    def test_message(self):
        self.assertContains(self.response, 'Conta marcada como paga!')
