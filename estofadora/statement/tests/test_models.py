# coding: utf-8
import datetime

from . import TestCase, Cash, create_cash


class CashModelTest(TestCase):

	def setUp(self):
		self.september = datetime.datetime(2015, 9, 10)

		self.october = datetime.datetime(2015, 10, 10)

		self.cash1 = create_cash(
			commit=True, history='Cash1', date=self.september.date(),
			expenses=100, income=50
		)
		self.cash2 = create_cash(
			commit=True, history='Cash2', date=self.september.date(),
			expenses=200, income=100
		)
		self.cash3 = create_cash(
			commit=True, history='Cash3', date=self.october.date(),
			expenses=300, income=150
		)		
		
		
	def tearDown(self):
		Cash.objects.all().delete()

	def test_total(self):
		expected_total = self.cash1.income - self.cash1.expenses
		self.assertEqual(self.cash1.total, expected_total)

		expected_total = self.cash2.income - self.cash2.expenses
		self.assertEqual(self.cash2.total, expected_total)

		expected_total = self.cash3.income - self.cash3.expenses
		self.assertEqual(self.cash3.total, expected_total)

	def test_total_value(self):
		expected_total = self.cash1.total + self.cash2.total + self.cash3.total

		self.assertEqual(Cash.total_value(), expected_total)

	def test_total_value_by_date(self):
		# cash1 and cash2 have the same date		
		expected_total = self.cash1.total + self.cash2.total

		date = self.september.date()
		self.assertEqual(Cash.total_value_by_date(date), expected_total)

	def test_total_value_by_month(self):
		expected_total = self.cash1.total + self.cash2.total

		date = self.september.date()
		self.assertEqual(Cash.total_value_by_month(date), expected_total)

	def test_filter_by_month(self):
		expected_items = 2

		date = self.september.date()
		self.assertEqual(len(Cash.filter_by_month(date)), expected_items)