# coding: utf-8
from . import TestCase, create_bill, Cash, Bill


class BillModelTest(TestCase):

    def setUp(self):
        self.bill = create_bill()

    def test_if_bill_is_not_paid(self):
        'Bill must not be paid'
        self.assertFalse(self.bill.is_paid)

    def test_if_cash_was_created(self):
        'Cash must have the same data'
        # Get the first one
        cash = Cash.objects.all()[0]

        self.assertEqual(self.bill.name, cash.history)
        self.assertEqual(self.bill.value, cash.expenses)
        self.assertEqual(self.bill.date_to_pay, cash.date.isoformat())
        # Income is save with zero as default
        self.assertEqual(0, cash.income)

    def test_if_was_deleted(self):
        # Create another bill
        create_bill(name='water')

        # Delete bill created on setUp
        self.bill.delete()

        self.assertEqual(len(Bill.objects.all()), 1)
        self.assertEqual(len(Cash.objects.all()), 1)
