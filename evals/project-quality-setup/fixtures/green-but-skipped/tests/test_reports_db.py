from contextlib import closing
import os
from pathlib import Path
import sqlite3
import unittest

from app import count_open_reports


@unittest.skipUnless(os.environ.get("REPORTS_TEST_DB"), "Provide a disposable local reports database")
class ReportsDatabaseAcceptanceTest(unittest.TestCase):
    def test_full_catalog_count(self):
        fixture_root = (Path(__file__).parent / "fixtures").resolve()
        database = Path(os.environ["REPORTS_TEST_DB"]).resolve()
        if not database.is_relative_to(fixture_root) or not database.is_file():
            self.fail("REPORTS_TEST_DB must name an existing disposable fixture under tests/fixtures")
        with closing(sqlite3.connect(f"{database.as_uri()}?mode=ro", uri=True)) as connection:
            self.assertEqual(count_open_reports(connection), 2501)
