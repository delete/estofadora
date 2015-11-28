# coding: utf-8
import datetime

from . import TestCase, Cash, create_cash


class CashModelTest(TestCase):

	def setUp(self):
		self.september = datetime.datetime(2015, 9, 10)

		self.october = datetime.datetime(2014, 10, 10)

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

		self.cash4 = create_cash(
			commit=True, history='Cash4', date=self.october.date(),
			expenses=400, income=200
		)
		
		
	def tearDown(self):
		Cash.objects.all().delete()

	def test_total(self):
		'''
			Test total from instanced object.
		'''
		expected_total = self.cash1.income - self.cash1.expenses
		self.assertEqual(self.cash1.total, expected_total)

		expected_total = self.cash2.income - self.cash2.expenses
		self.assertEqual(self.cash2.total, expected_total)

		expected_total = self.cash3.income - self.cash3.expenses
		self.assertEqual(self.cash3.total, expected_total)

	def test_total_value(self):
		'''
			Test total from all objects.
		'''
		expected_total = (
			self.cash1.total + self.cash2.total + 
			self.cash3.total + self.cash4.total
		)

		self.assertEqual(Cash.total_value(), expected_total)

	def test_list_years(self):
		expected_items = [2014, 2015]

		self.assertEqual(Cash.list_years(), expected_items)

	def test_filter_by_date_by_year(self):
		# Filter by year = 2014 must return 2 items
		expected_items = 2

		items = Cash.filter_by_date(year=2014)

		self.assertEqual(len(items), expected_items)

	def test_filter_by_date_by_month(self):
		# Filter by month = 10 must return 2 items
		expected_items = 2

		items = Cash.filter_by_date(month=10)

		self.assertEqual(len(items), expected_items)

	def test_filter_by_date_by_day(self):
		#Filter by day = 11 must return 0 items
		expected_items = 0

		items = Cash.filter_by_date(day=11)

		self.assertEqual(len(items), expected_items)

	def test_total_value_by_date_by_year(self):
		#Filter by year = 2014
		expected_total = self.cash3.total + self.cash4.total

		year = 2014
		self.assertEqual(Cash.total_value_by_date(year=year), expected_total)

	def test_total_value_by_date_by_month_and_year(self):
		#Filter by month and year = 09/2014
		expected_total = self.cash1.total + self.cash2.total

		month = 9
		year = 2015
		total = Cash.total_value_by_date(month=month, year=year)
		self.assertEqual(total, expected_total)

	def test_total_value_by_date_by_day(self):
		#Filter by day = 11/10/2014
		expected_total = self.cash3.total + self.cash4.total

		day = 10
		month = 10
		year = 2014
		total = Cash.total_value_by_date(day=day, month=month, year=year)
		self.assertEqual(total, expected_total)
