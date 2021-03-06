from datetime import datetime, date, timedelta
import unittest

from businesstime import BusinessTime, USFederalHolidays


class BusinessTimeTest(unittest.TestCase):

    def setUp(self):
        """
        Tests mostly based around January 2014, where two holidays, New Years Day
        and MLK day, fall on the 1st and 20th, respectively.

            January 2014
        Su Mo Tu We Th Fr Sa
                  1  2  3  4
         5  6  7  8  9 10 11
        12 13 14 15 16 17 18
        19 20 21 22 23 24 25
        26 27 28 29 30 31
        """
        self.bt = BusinessTime(holidays=USFederalHolidays())

    def test_iterdays(self):
        start = datetime(2014, 1, 16)
        end = datetime(2014, 1, 22)
        self.assertEqual(
            tuple(self.bt.iterdays(start, end)),
            (
                datetime(2014, 1, 16),
                datetime(2014, 1, 17),
                datetime(2014, 1, 18),
                datetime(2014, 1, 19),
                datetime(2014, 1, 20),
                datetime(2014, 1, 21)
            )
        )

    def test_iterdays_same_day(self):
        start = datetime(2014, 1, 16, 12, 15)
        end = datetime(2014, 1, 16, 12, 16)
        self.assertEqual(
            tuple(self.bt.iterdays(start, end)),
            (
                datetime(2014, 1, 16),
            )
        )

    def test_iterdays_clears_time(self):
        start = datetime(2014, 1, 16, 12, 12, 11)
        end = datetime(2014, 1, 18, 15)
        self.assertEqual(
            tuple(self.bt.iterdays(start, end)),
            (
                datetime(2014, 1, 16),
                datetime(2014, 1, 17)
            )
        )

    def test_iterweekdays(self):
        start = datetime(2014, 1, 16)
        end = datetime(2014, 1, 22)
        self.assertEqual(
            tuple(self.bt.iterweekdays(start, end)),
            (
                datetime(2014, 1, 16),
                datetime(2014, 1, 17),
                datetime(2014, 1, 20),
                datetime(2014, 1, 21)
            )
        )

    def test_iterbusinessdays(self):
        start = datetime(2014, 1, 16)
        end = datetime(2014, 1, 22)
        self.assertEqual(
            tuple(self.bt.iterbusinessdays(start, end)),
            (
                datetime(2014, 1, 16),
                datetime(2014, 1, 17),
                datetime(2014, 1, 21)
            )
        )

    def test_iterbusinessdays_conforms_to_business_hours(self):
        start = datetime(2014, 1, 16, 17, 1)
        end = datetime(2014, 1, 23, 2)
        self.assertEqual(
            tuple(self.bt.iterbusinessdays(start, end)),
            (
                datetime(2014, 1, 17),
                datetime(2014, 1, 21),
                datetime(2014, 1, 22)
            )
        )

    def test_isduringbusinessday(self):
        self.assertTrue(self.bt.isduringbusinesshours(datetime(2014, 1, 15, 12)))
        self.assertFalse(self.bt.isduringbusinesshours(datetime(2014, 1, 15)))
        self.assertFalse(self.bt.isduringbusinesshours(datetime(2014, 1, 18, 11)))
        self.assertFalse(self.bt.isduringbusinesshours(datetime(2014, 1, 20, 11, 46, 43)))

    def test_holidays_specified_as_list(self):
        bd = BusinessTime(holidays=[date(2014, 1, 1)])
        self.assertTrue(bd.isholiday(date(2014, 1, 1)))
        self.assertFalse(bd.isholiday(date(2014, 1, 2)))

    def test_businesstimedelta_after_during(self):
        start = datetime(2014, 1, 16, 18, 30)
        end = datetime(2014, 1, 22, 10, 0)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=2, hours=1)
        )

    def test_businesstimedelta_nonbusiness_after(self):
        start = datetime(2014, 1, 12, 12)
        end = datetime(2014, 1, 17, 19, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=4, hours=8)
        )

    def test_businesstimedelta_before_after(self):
        start = datetime(2014, 1, 13, 4)
        end = datetime(2014, 1, 17, 19, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=4, hours=8)
        )

    def test_businesstimedelta_during_after(self):
        start = datetime(2014, 1, 30, 12, 15)
        end = datetime(2014, 1, 31, 19, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=1, hours=4, minutes=45)
        )

    def test_businesstimedelta_during_before(self):
        start = datetime(2014, 8, 4, 11)
        end = datetime(2014, 8, 6, 5)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=1, hours=6)
        )

    def test_businesstimedelta_before_before(self):
        start = datetime(2014, 8, 4, 1)
        end = datetime(2014, 8, 4, 5)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=0)
        )

    def test_businesstimedelta_after_after(self):
        start = datetime(2014, 8, 4, 22)
        end = datetime(2014, 8, 4, 23)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=0)
        )

    def test_businesstimedelta_during_nonbusiness(self):
        start = datetime(2014, 1, 10, 16, 15)
        end = datetime(2014, 1, 12, 12, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(minutes=45)
        )

    def test_businesstimedelta_during_nonbusiness2(self):
        start = datetime(2014, 1, 9, 16, 15)
        end = datetime(2014, 1, 12, 12, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=1, minutes=45)
        )

    def test_businesstimedelta_after_nonbusiness(self):
        start = datetime(2014, 1, 10, 17, 15)
        end = datetime(2014, 1, 12, 12, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta()
        )

    def test_businesstimedelta_during_during(self):
        start = datetime(2014, 1, 2, 9, 12)
        end = datetime(2014, 1, 3, 9, 10)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(hours=7, minutes=58)
        )

    def test_businesstimedelta_during_during2(self):
        start = datetime(2014, 1, 2, 9, 10)
        end = datetime(2014, 1, 3, 9, 12)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=1, minutes=2)
        )

    def test_businesstimedelta_during_during3(self):
        start = datetime(2014, 1, 2, 9, 10)
        end = datetime(2014, 1, 2, 9, 12)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(minutes=2)
        )

    def test_businesstimedelta_nonbusiness_nonbusiness(self):
        start = datetime(2014, 1, 4, 9, 10)
        end = datetime(2014, 1, 4, 9, 12)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta()
        )

    def test_businesstimedelta_exactly_one_day(self):
        start = datetime(2014, 1, 7, 10)
        end = datetime(2014, 1, 8, 10)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=1)
        )

    def test_businesstimedelta_exactly_one_day2(self):
        """
        Test for https://github.com/seatgeek/businesstime/issues/3
        """
        start = datetime(2014, 1, 7, 9)
        end = datetime(2014, 1, 8, 9)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=1)
        )


class USFederalHolidaysTest(unittest.TestCase):

    def test_2013(self):
        holidays_gen = USFederalHolidays()
        self.assertEqual(
            list(holidays_gen(date(2013, 1, 1), end=date(2013, 12, 31))),
            [
                date(2013, 1, 1),
                date(2013, 1, 21),
                date(2013, 2, 18),
                date(2013, 5, 27),
                date(2013, 7, 4),
                date(2013, 9, 2),
                date(2013, 10, 14),
                date(2013, 11, 11),
                date(2013, 11, 28),
                date(2013, 12, 25)
            ]
        )

    def test_2014(self):
        holidays_gen = USFederalHolidays()
        self.assertEqual(
            list(holidays_gen(date(2014, 1, 1), end=date(2014, 12, 31))),
            [
                date(2014, 1, 1),
                date(2014, 1, 20),
                date(2014, 2, 17),
                date(2014, 5, 26),
                date(2014, 7, 4),
                date(2014, 9, 1),
                date(2014, 10, 13),
                date(2014, 11, 11),
                date(2014, 11, 27),
                date(2014, 12, 25)
            ]
        )
