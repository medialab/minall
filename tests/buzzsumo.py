import sys
import unittest
from pathlib import Path

import casanova

from minall.enrichment.buzzsumo.get_data import get_buzzsumo_data
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


class TestBuzzsumo(unittest.TestCase):
    CONFIG = Path()
    OUTFILE = Path.cwd().joinpath("tests").joinpath("test.csv")

    def setUp(self):
        if not self.CONFIG.is_file():
            config = None
        else:
            config = str(self.CONFIG)
        self.keys = APIKeys(config)

    def test_match(self):
        assert self.keys.buzzsumo_token is not None
        data = [
            "https://www.lemonde.fr/idees/article/2023/10/23/maintenir-la-pression-pour-lutter-contre-l-evasion-fiscale_6196088_3232.html"
        ]
        get_buzzsumo_data(
            data=data, token=self.keys.buzzsumo_token, outfile=self.OUTFILE
        )
        with casanova.reader(self.OUTFILE) as reader:
            row = reader.__next__()
            row_dict = dict(zip(LinksConstants.col_names, row))
            for c in EXPECTED_VALUES:
                try:
                    assert row_dict[c] != ""
                except AssertionError:
                    raise AssertionError(f"\nMissing expected value in column {c}")
        self.OUTFILE.unlink()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestBuzzsumo.CONFIG = Path(sys.argv.pop())
    unittest.main()
