from . import TestBase, datetime

from estofadora.core.utils import last_day_of, month_before_of


class TestLastDayOf(TestBase):

    def test_last_day_of_a_year(self):
        # Last day from 2015
        expected = datetime.datetime(2015, 12, 31).date()

        result = last_day_of(year=2015, month=12)

        self.assertEqual(expected, result)

    def test_last_day_from_february(self):
        expected = datetime.datetime(2015, 2, 28).date()

        result = last_day_of(year=2015, month=2)

        self.assertEqual(expected, result)


class TestGetMonthBefore(TestBase):

    def test_first_month_of_a_year(self):
        # December
        expected = 2015, 12

        result = month_before_of(year=2016, month=1)

        self.assertEqual(expected, result)

    def test_month(self):
        # February
        expected = 2015, 2

        result = month_before_of(year=2015, month=3)

        self.assertEqual(expected, result)
