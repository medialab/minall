import unittest
from pathlib import Path

import casanova
from base import BaseTest

from minall.enrichment.buzzsumo.get_data import get_buzzsumo_data, yield_buzzsumo_data
from minall.tables.links.constants import LinksConstants
from minall.utils.parse_config import APIKeys

EXPECTED_VALUES = [
    "domain",
    "twitter_share",
    "facebook_share",
    "title",
    "date_published",
    "pinterest_share",
    "facebook_comment",
    "reddit_engagement",
]

TEST_DATA = [
    "https://www.lemonde.fr/idees/article/2023/10/23/maintenir-la-pression-pour-lutter-contre-l-evasion-fiscale_6196088_3232.html"
]

OUTFILE = Path(__file__).parent.joinpath("test.csv")


class TestBuzzsumo(BaseTest):
    def setUp(self) -> None:
        self.keys = APIKeys(self.config)

    def test_expected_values(self) -> None:
        assert self.keys.buzzsumo_token
        get_buzzsumo_data(
            data=TEST_DATA, token=self.keys.buzzsumo_token, outfile=OUTFILE
        )
        with casanova.reader(OUTFILE) as reader:
            row = reader.__next__()
            row_dict = dict(zip(LinksConstants.col_names, row))
            for c in EXPECTED_VALUES:
                try:
                    self.assertNotEqual(row_dict[c], "")
                except AssertionError:
                    raise AssertionError(f"Missing expected value in column {c}")

    def test_repeated_calls(self) -> None:
        assert self.keys.buzzsumo_token
        data = [TEST_DATA[0] for _ in range(20)]
        unique_results = set()
        for result in yield_buzzsumo_data(token=self.keys.buzzsumo_token, data=data):
            unique_results.add(tuple(result.as_csv_row()))
        try:
            self.assertEqual(len(unique_results), 1)
        except AssertionError:
            print(unique_results)
            raise AssertionError

    def tearDown(self) -> None:
        if OUTFILE.is_file():
            OUTFILE.unlink()
        return super().tearDown()


if __name__ == "__main__":
    unittest.main(buffer=False)
