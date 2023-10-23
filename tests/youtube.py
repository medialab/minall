import csv
import json
import os
import sys
import unittest
from pathlib import Path

from minall.enrichment.youtube.get_data import get_youtube_data

CHANNEL_CHECK = [
    "identifier",
    "date_published",
    "country_of_origin",
    "abstract",
    "keywords",
    "title",
    "youtube_subscribe",
    "create_video",
]

VIDEO_CHECK = [
    "date_published",
    "duration",
    "title",
    "abstract",
    "youtube_watch",
    "youtube_comment",
    "youtube_like",
    "creator_type",
    "creator_location_created",
    "creator_identifier",
    "creator_youtube_subscribe",
    "creator_create_video",
    "creator_name",
]


class TestYouTube(unittest.TestCase):
    CONFIG = Path.cwd().joinpath("config.json")
    OUTFILE = Path.cwd().joinpath("tests").joinpath("test.csv")

    def setUp(self):
        if self.CONFIG.is_file():
            with open(self.CONFIG) as f:
                config = json.load(f)
            self.key = config["youtube"]["key"]
        else:
            self.key = os.getenv("YOUTUBE_KEY")

    def test_channel(self):
        assert self.key is not None
        data = [(str("https://www.youtube.com/@sciencespo"), str("LINK-ID"))]
        get_youtube_data(data=data, keys=[self.key], outfile=self.OUTFILE)
        with open(self.OUTFILE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for field in CHANNEL_CHECK:
                    try:
                        assert row[field] != ""
                    except AssertionError as e:
                        print(f"\nMissing {field}")
                        raise e
                break
        self.OUTFILE.unlink()

    def test_video(self):
        assert self.key is not None
        data = [(str("https://www.youtube.com/watch?v=DrAUDPShQRg"), str("ID"))]
        get_youtube_data(data=data, keys=[self.key], outfile=self.OUTFILE)
        with open(self.OUTFILE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for field in VIDEO_CHECK:
                    assert row[field] is not None
                break
        self.OUTFILE.unlink()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestYouTube.CONFIG = Path(sys.argv.pop())
    unittest.main(buffer=True)
