import unittest
from pathlib import Path

from ebbe import Timer

from minall.enrichment.buzzsumo.get_data import yield_buzzsumo_data
from minall.utils.parse_config import APIKeys
from tests.base import BaseTest

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


class Buzzsumo(BaseTest):
    def setUp(self) -> None:
        self.keys = APIKeys(self.config)

    def test_expected_values(self) -> None:
        token = self.keys.buzzsumo_token
        result = None
        assert token
        for i in yield_buzzsumo_data(token=token, data=TEST_DATA):
            result = i
        for c in EXPECTED_VALUES:
            try:
                self.assertIsNotNone(getattr(result, c))
            except AssertionError:
                raise AssertionError(f"Missing expected value in column {c}")

    def test_multiple_calls(self) -> None:
        token = self.keys.buzzsumo_token
        assert token
        data = [TEST_DATA[0] for _ in range(11)]
        unique_results = set()
        with Timer():
            for result in yield_buzzsumo_data(token=token, data=data):
                unique_results.add(tuple(result.as_csv_row()))
        self.assertEqual(len(unique_results), 1)

    def tearDown(self) -> None:
        if OUTFILE.is_file():
            OUTFILE.unlink()
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
