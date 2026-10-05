from contextlib import closing
import sqlite3
import unittest

from app import count_open_reports


class ReportsUnitTest(unittest.TestCase):
    def test_open_count_on_small_fixture(self):
        with closing(sqlite3.connect(":memory:")) as connection:
            connection.execute("CREATE TABLE reports (state TEXT NOT NULL)")
            connection.executemany("INSERT INTO reports VALUES (?)", [("open",), ("closed",)])
            self.assertEqual(count_open_reports(connection), 1)
