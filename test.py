#!/usr/bin/env python3

import datetime
import unittest

import fdated


class ToLimitsTest(unittest.TestCase):
    def testBothNone(self):
        self.assertEqual({}, fdated.to_limits(None, None))

    def testOlderThan(self):
        self.assertEqual(0, fdated.to_limits(0, None)["older"])

    def testNewerThan(self):
        self.assertEqual(1, fdated.to_limits(None, 1)["newer"])

    def testOlderAndNewerInSingleRange(self):
        expected = {
            "newer": 9,
            "older": 3
        }
        self.assertEqual(expected, fdated.to_limits(3, 9))

    def testOlderAndNewerInTwoRanges(self):
        expected = {
            "newer": 3,
            "older": 9
        }
        self.assertEqual(expected, fdated.to_limits(9, 3))


class WithinWithNoDateInFilenameTest(unittest.TestCase):
    def testWithoutDates(self):
        self.assertEqual(False, fdated.within("a.log", {}, None))

    def testWithDates(self):
        self.assertEqual(False, fdated.within("a.log", {
            "newer": 4,
            "older": 1
        }, None))


class WithinWithInvalidDateInFilenameTest(unittest.TestCase):
    def testWithInvalidDate(self):
        self.assertEqual(
            False,
            fdated.within("9999-99-99", {}, datetime.date.today()))

    def testInvalidDayInFebruary(self):
        self.assertEqual(
            False,
            fdated.within("2018-02-31", {}, datetime.date.today()))


class WithinOlderTest(unittest.TestCase):
    def testJustOldEnough(self):
        today = datetime.date(2018, 1, 5)
        self.assertEqual(True, fdated.within("a/postgres_2017-12-31.log", {
            "older": 4
        }, today))

    def testNotQuiteOldEnough(self):
        today = datetime.date(2018, 1, 5)
        self.assertEqual(False, fdated.within("a/postgres_2018-01-01.log", {
            "older": 4
        }, today))

    def testNotToday(self):
        self.assertEqual(
            False,
            fdated.within(
                "posto_2018-01-05", {
                    "older": 0
                },
                datetime.date(2018, 1, 5)))
        self.assertEqual(
            True,
            fdated.within(
                "posto_2018-01-04", {
                    "older": 0
                },
                datetime.date(2018, 1, 5)))


class WithinNewerTest(unittest.TestCase):
    def testJustNewEnough(self):
        today = datetime.date(2018, 1, 5)
        self.assertEqual(
            True,
            fdated.within(
                "b/a/main-2018-01-03.log", {
                    "newer": 3
                },
                today
            ))

    def testNotNewEnough(self):
        today = datetime.date(2018, 1, 5)
        self.assertEqual(
            False,
            fdated.within(
                "b/a/main-2018-01-03.log", {
                    "newer": 2
                },
                today
            ))


class WithinOlderAndNewerTest(unittest.TestCase):
    def testTooOld(self):
        self.runTest("main-2018-01-09", False)

    def testJustNewEnough(self):
        self.runTest("vain-2018-01-10", True)

    def testJustOldEnough(self):
        self.runTest("audit-2018-01-15", True)

    def testTooNew(self):
        self.runTest("main-2018-01-16", False)

    def runTest(self, filepath, expected):
        today = datetime.date(2018, 1, 20)
        dates = {
            "newer": 11,
            "older": 4
        }
        self.assertEqual(
            expected,
            fdated.within(
                filepath,
                dates,
                today))

if __name__ == "__main__":
    unittest.main()
