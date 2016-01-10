from . import TestBase, datetime

from estofadora.core.utils import get_last_day


class TestGetLastDay(TestBase):

    def test_last_day_of_a_year(self):
        # Last day from 2015
        expected = datetime.datetime(2015, 12, 31).date()

        result = get_last_day(year=2016, month=1)

        self.assertEqual(expected, result)

    def test_last_day_from_february(self):
        expected = datetime.datetime(2015, 2, 28).date()

        result = get_last_day(year=2015, month=3)

        self.assertEqual(expected, result)
