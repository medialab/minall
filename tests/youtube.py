import csv
import unittest
from pathlib import Path

from minall.enrichment.youtube.get_data import get_youtube_data
from minall.utils.parse_config import APIKeys
from tests.base import BaseTest

SHORT = "https://www.youtube.com/shorts/Aw1nBBK8z24"


class YTest(BaseTest):
    links_outfile = Path(__file__).parent.joinpath("links.csv")

    def setUp(self) -> None:
        keys = APIKeys(self.config)
        self.key = keys.youtube_key

    def test_short(self):
        # Do Enrichment
        get_youtube_data(
            data=[SHORT],
            keys=self.key,  # type:ignore
            outfile=self.links_outfile,
        )

        # Check results
        with open(self.links_outfile) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.assertEqual(row["domain"], "youtube.com")
                self.assertNotEqual(row["title"], "")

    def tearDown(self):
        if self.links_outfile.is_file():
            Path.unlink(self.links_outfile)


if __name__ == "__main__":
    unittest.main()
