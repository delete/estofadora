# coding: utf-8
import datetime

from django.core.urlresolvers import reverse


from . import (
    TestBase, ContactForm, Contact, create_contact,
    create_item, create_picture, create_client, create_bill
)


class HomeViewTest(TestBase):

    def setUp(self):
        self.login()
        self.url = reverse('core:home')
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_get_logout(self):
        self._test_get_logout(self.url)

    def test_boards_content_empty(self):
        self.assertContains(self.response, '"announcement-heading">0<', 4)

    def test_boards_content_when_not_empty(self):
        client = create_client(commit=True)

        item1 = create_item(client=client, commit=True)
        create_picture(item=item1)

        create_item(client=client, commit=True)
        create_bill(commit=True)

        self.response = self.client.get(self.url)
        # one client, one picture and one bill
        self.assertContains(self.response, '"announcement-heading">1<', 3)
        # two items
        self.assertContains(self.response, '"announcement-heading">2<', 1)

    def test_week_delivery_content_when_empty(self):
        self.assertContains(self.response, 'Nenhuma entrega para essa semana.')

    def test_week_delivery_content_when_not_empty(self):
        client = create_client(commit=True)

        today = datetime.datetime.now()

        item1 = create_item(client=client, delivery_date=today, commit=True)
        item2 = create_item(
            client=client, delivery_date=today, concluded=True, commit=True
        )
        item3 = create_item(client=client, name='Puff', commit=True)

        self.response = self.client.get(self.url)

        # Item1 should appear and its status is concluded False
        self.assertContains(self.response, item1.name)
        self.assertContains(self.response, item1.client.name)
        self.assertContains(self.response, 'Pendente')

        # Item2 should appear and its status is concluded True
        self.assertContains(self.response, item2.name)
        self.assertContains(self.response, item2.client.name)
        self.assertContains(self.response, 'Entregue')

        # Item3 must not appear
        self.assertNotContains(self.response, item3.name)

    def test_week_bills_content_when_empty(self):
        self.assertContains(self.response, 'Nenhuma conta para essa semana.')

    def test_week_bills_content_when_not_empty(self):
        today = datetime.datetime.now()
        bill1 = create_bill(value=11, date_to_pay=today, commit=True)
        bill2 = create_bill(
            name='Net', date_to_pay=today, value=44, is_paid=True, commit=True
        )
        bill3 = create_bill(name='Luz', value=33, commit=True)

        # Bill1 belong this week number
        self.response = self.client.get(self.url)
        self.assertContains(self.response, bill1.name)
        self.assertContains(self.response, bill1.value)
        self.assertContains(self.response, 'Pendente')

        # Bill2 belong this week number too
        self.assertContains(self.response, bill2.name)
        self.assertContains(self.response, bill2.value)
        self.assertContains(self.response, 'Pago')

        # Bill3 does not belong this week.
        self.assertNotContains(self.response, bill3.name)
        self.assertNotContains(self.response, bill3.value)


class SiteViewTest(TestBase):

    def setUp(self):
        self.item = create_item(commit=True)
        self.picture1 = create_picture(self.item, public=True, state='after')
        self.picture2 = create_picture(self.item, public=True, state='after')
        self.picture3 = create_picture(self.item, public=True, state='after')
        self.picture4 = create_picture(self.item, public=True, state='after')
        self.picture5 = create_picture(self.item, public=True)

        self.response = self.client.get(reverse('core:site'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'site/site_index.html')

    def test_if_has_login_url(self):
        self.assertContains(self.response, reverse('login:login'))

    def test_url_in_content(self):
        # Picture 1,2,3 and 4 must appear, because they are public=True
        self.assertContains(self.response, self.picture1.image.url)
        self.assertContains(self.response, self.picture2.image.url)
        self.assertContains(self.response, self.picture3.image.url)
        self.assertContains(self.response, self.picture4.image.url)

        # Picture 5 must not appear, because it is public=False
        self.assertNotContains(self.response, self.picture5.image.url)


class PortfolioViewTest(TestBase):

    def setUp(self):
        self.item = create_item(commit=True)
        self.picture1 = create_picture(self.item, public=True)
        self.picture2 = create_picture(self.item, public=True)
        self.picture3 = create_picture(self.item, public=False)

        self.response = self.client.get(reverse('core:portfolio'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'site/portfolio.html')

    def test_url_in_content(self):
        # Picture 1 and 2 must appear, because they are public=True
        self.assertContains(self.response, self.item.name)
        self.assertContains(self.response, self.picture1.image.url)
        self.assertContains(self.response, self.picture2.image.url)

        # Picture 3 must not appear, because it is public=False
        self.assertNotContains(self.response, self.picture3.image.url)


class ContactViewTest(TestBase):

    def setUp(self):
        self.response = self.client.get(reverse('core:contact'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'site/contact.html')

    def test_context(self):
        self.assertContains(self.response, '<iframe')

    def test_if_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, ContactForm)

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="submit"')


class ContactPostTest(TestBase):

    def setUp(self):
        data = create_contact(commit=False)
        self.response = self.client.post(
                reverse('core:contact'), data, follow=True
            )

    def test_message(self):
        self.assertContains(
            self.response, 'Obrigado pela mensagem, entraremos em contato!'
        )

    def test_if_saved(self):
        self.assertTrue(Contact.objects.exists())

    def test_redirect(self):
        expected_url = reverse('core:contact')

        self.assertRedirects(
            self.response, expected_url, status_code=302,
            target_status_code=200
        )


class ContactMessagesViewTest(TestBase):

    def setUp(self):
        self.login()

        self.contactMessage = create_contact(commit=True)

        self.url = reverse('core:contactMessages')
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'contactMessages.html')

    def test_get_logout(self):
        self._test_get_logout(self.url)

    def test_content(self):
        self.assertContains(self.response, self.contactMessage.name)
        self.assertContains(self.response, self.contactMessage.subject)
        self.assertContains(self.response, self.contactMessage.email)
        self.assertContains(self.response, self.contactMessage.telephone)
        self.assertContains(self.response, self.contactMessage.description)

    def test_empty(self):
        Contact.objects.all().delete()

        self.response = self.client.get(self.url)
        self.assertContains(self.response, 'Nenhuma mensagem!')


class DeleteMensagemViewTest(TestBase):

    def setUp(self):
        self.login()

        self.contactMessage1 = create_contact(commit=True)

        self.contactMessage2 = create_contact(commit=True)

        # Must have 2 messages before post.
        self.assertEqual(len(Contact.objects.all()), 2)

        self.url = reverse(
                'core:deleteMessage', args=[self.contactMessage1.pk]
            )
        self.response = self.client.post(self.url, follow=True)

    def test_get_logout(self):
        self._test_get_logout(self.url)

    def test_redirect(self):
        expected_url = reverse('core:contactMessages')

        self.assertRedirects(
            self.response, expected_url, status_code=302,
            target_status_code=200
        )

    def test_if_deleted(self):
        self.assertEqual(len(Contact.objects.all()), 1)

    def test_message(self):
        self.assertContains(self.response, 'Mensagem removida com sucesso!')


class MarkAsReadMensagemViewTest(TestBase):

    def setUp(self):
        self.login()

        self.contactMessage1 = create_contact(commit=True)

        # read must start as False
        self.assertFalse(self.contactMessage1.read)

        self.url = reverse(
                'core:markMessageAsRead', args=[self.contactMessage1.pk]
            )
        self.response = self.client.post(self.url, follow=True)

    def test_get_logout(self):
        self._test_get_logout(self.url)

    def test_redirect(self):
        expected_url = reverse('core:contactMessages')

        self.assertRedirects(
            self.response, expected_url, status_code=302,
            target_status_code=200
        )

    def test_if_deleted(self):
        contact = Contact.objects.get(pk=self.contactMessage1.pk)
        self.assertTrue(contact.read)

    def test_message(self):
        self.assertContains(self.response, 'Mensagem lida!')
