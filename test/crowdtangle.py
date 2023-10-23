import csv
import json
import sys
import unittest
from pathlib import Path

from minall.enrichment.crowdtangle.get_data import get_facebook_post_data

data = {}
POST_CHECK = list(
    {
        "domain": "facebook.com",
        "type": "SocialMediaPosting",
        "identifier": data.get("id"),
        "date_published": data.get("date"),
        "date_modified": data.get("updated"),
        "text": data.get("message"),
        "creator_type": "defacto:SocialMediaAccount",
        "creator_identifier": data.get("account_id"),
        "creator_facebook_subscribe": data.get("account_subscriber_count"),
        "creator_name": data.get("account_name"),
        "creator_url": data.get("account_url"),
        "facebook_comment": data.get("actual_comment_count"),
        "facebook_like": data.get("actual_like_count"),
        "facebook_share": data.get("actual_share_count"),
    }.keys()
)


class TestFacebook(unittest.TestCase):
    CONFIG = Path.cwd().joinpath("config.json")
    LINKS_OUTFILE = Path.cwd().joinpath("test").joinpath("appearances.csv")
    SHARED_CONTENT_OUTFILE = Path.cwd().joinpath("test").joinpath("shared_content.csv")

    def setUp(self):
        with open(self.CONFIG) as f:
            config = json.load(f)
            self.token = config["crowdtangle"]["token"]

    def test_post(self):
        data = [
            (
                str(
                    "https://www.facebook.com/groups/960617117610735/permalink/1544671352538639/"
                ),
                str("LINK-ID"),
            )
        ]
        get_facebook_post_data(
            data=data,
            appearances_outfile=self.LINKS_OUTFILE,
            token=self.token,
            rate_limit=50,
            shared_content_outfile=self.SHARED_CONTENT_OUTFILE,
        )
        with open(self.LINKS_OUTFILE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for field in POST_CHECK:
                    try:
                        assert row[field] != ""
                    except AssertionError as e:
                        print(f"\nMissing {field}")
                        raise e
                break
        self.LINKS_OUTFILE.unlink()
        self.SHARED_CONTENT_OUTFILE.unlink()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestFacebook.CONFIG = Path(sys.argv.pop())
    unittest.main(buffer=True)
