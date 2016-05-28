# coding: utf-8
from django.db import IntegrityError, transaction

from . import TestCase, ModelClient, create_client


class ClientModelTest(TestCase):

    def setUp(self):
        self.client = create_client()

    def tearDown(self):
        ModelClient.objects.all().delete()

    def test_if_client_is_active(self):
        self.assertTrue(self.client.is_active)

    def test_duplicate_email(self):
        with transaction.atomic():
            data = create_client(name='Andre', commit=False)
            c = ModelClient(**data)
            self.assertRaises(IntegrityError, c.save)

        self.assertEqual(len(ModelClient.objects.all()), 1)
