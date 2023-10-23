import csv
import json
import os
import sys
import unittest
from pathlib import Path

from minall.enrichment.buzzsumo.get_data import get_buzzsumo_data

data = {}
FIELD_CHECK = list(
    {
        "twitter_share": data.get("twitter_shares"),
        "facebook_share": data.get("total_facebook_shares"),
        "title": data.get("title"),
        "date_published": None,
        "pinterest_share": data.get("pinterest_shares"),
        # "creator_name": data.get("author_name"),
        # "creator_identifier": data.get("twitter_user_id"),
        # "duration": data.get("video_length"),
        "facebook_comment": data.get("facebook_comments"),
        # "youtube_watch": data.get("youtube_views"),
        # "youtube_like": data.get("youtube_likes"),
        # "youtube_comment": data.get("youtube_comments"),
        # "tiktok_share": data.get("tiktok_share_count"),
        # "tiktok_comment": data.get("tiktok_comment_count"),
        "reddit_engagement": data.get("total_reddit_engagements"),
    }.keys()
)


class TestBuzzsumo(unittest.TestCase):
    CONFIG = Path()
    OUTFILE = Path.cwd().joinpath("tests").joinpath("test.csv")

    def setUp(self):
        if self.CONFIG.is_file():
            with open(self.CONFIG) as f:
                config = json.load(f)
            self.token = config["buzzsumo"]["token"]
        else:
            self.token = os.getenv("BUZZSUMO_TOKEN")

    def test_result(self):
        assert self.token is not None
        data = [
            (
                str(
                    "https://www.lemonde.fr/idees/article/2023/10/23/maintenir-la-pression-pour-lutter-contre-l-evasion-fiscale_6196088_3232.html"
                ),
                str("LINK-ID"),
            )
        ]
        get_buzzsumo_data(data=data, outfile=self.OUTFILE, token=self.token)
        with open(self.OUTFILE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for field in FIELD_CHECK:
                    try:
                        assert row[field] != ""
                    except AssertionError as e:
                        print(f"\nMissing {field}")
                        raise e
                break
        self.OUTFILE.unlink()

    def test_no_result(self):
        assert self.token is not None
        data = [
            (
                str("https://medialab.github.io/"),
                str("LINK-ID"),
            )
        ]
        get_buzzsumo_data(data=data, outfile=self.OUTFILE, token=self.token)
        with open(self.OUTFILE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for field in FIELD_CHECK:
                    assert row[field] == ""
                break
        self.OUTFILE.unlink()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestBuzzsumo.CONFIG = Path(sys.argv.pop())
    unittest.main(buffer=True)
