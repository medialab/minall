import csv
import unittest
from pathlib import Path

from minall.tables.links import LinksTable
from minall.tables.shared_content import SharedContentTable
from minall.utils.database import connect_to_database
from tests.base import BaseTest


class TableTest(BaseTest):
    def setUp(self) -> None:
        self.conn = connect_to_database()

    def test_links(self):
        # Produce test data
        with open(INFILE, "w") as f:
            writer = csv.writer(f)
            writer.writerows(LINKS_INPUT)

        # Generate the table using an in-file
        table = LinksTable(
            conn=self.conn, infile=INFILE, url_col="target_url", outfile=OUTFILE
        )

        # Simulate enrichment and update table with new data
        with open(OUTFILE, "w") as f:
            writer = csv.writer(f)
            writer.writerows(LINKS_ENRICHMENT)
        table.update_from_csv(datafile=OUTFILE)

        # Export the updated table
        table.export()
        with open(OUTFILE, "r") as f:
            reader = csv.DictReader(f)
            export = [row for row in reader]

        # Check exported data against expected data
        self.assertEqual(export, LINKS_EXPORT)

    def test_shared_content(self):
        # Produce test data
        with open(INFILE, "w") as f:
            writer = csv.writer(f)
            writer.writerows(SHARED_CONTENT_INPUT)

        # Generate the table using an in-file
        table = SharedContentTable(conn=self.conn, infile=INFILE, outfile=OUTFILE)

        # Simulate enrichment and update table with new data
        with open(OUTFILE, "w") as f:
            writer = csv.writer(f)
            writer.writerows(SHARED_CONTENT_ENRICHMENT)
        table.update_from_csv(datafile=OUTFILE)
        update = table.select_from("*")

        # Check result against expected result
        self.assertEqual(update, SHARED_CONTENT_UPDATE)

    def tearDown(self):
        INFILE.unlink()
        OUTFILE.unlink()


INFILE = Path(__file__).parent.joinpath("infile.csv")
LINKS_INPUT = [
    ["target_url"],
    ["https://www.facebook.com/100063820962754/posts/721047780032581"],
    ["https://www.github/medialab/minall"],
]
SHARED_CONTENT_INPUT = [
    ["post_url", "content_url"],
    ["facebook1", "image1"],
    ["facebook1", "image2"],
]

OUTFILE = Path(__file__).parent.joinpath("newfile.csv")
LINKS_ENRICHMENT = [
    ["url", "domain"],
    ["https://www.facebook.com/100063820962754/posts/721047780032581", "facebook.com"],
]
SHARED_CONTENT_ENRICHMENT = [
    ["post_url", "content_url", "media_type"],
    ["facebook1", "image1", "PhotoObject"],
    ["facebook1", "image2", "PhotoObject"],
]

SHARED_CONTENT_UPDATE = [
    ("facebook1", "image1", "PhotoObject", None, None),
    ("facebook1", "image2", "PhotoObject", None, None),
]


LINKS_EXPORT = [
    {
        "target_url": "https://www.facebook.com/100063820962754/posts/721047780032581",
        "url": "https://www.facebook.com/100063820962754/posts/721047780032581",
        "domain": "facebook.com",
        "work_type": "",
        "duration": "",
        "identifier": "",
        "date_published": "",
        "date_modified": "",
        "country_of_origin": "",
        "abstract": "",
        "keywords": "",
        "title": "",
        "text": "",
        "hashtags": "",
        "creator_type": "",
        "creator_date_created": "",
        "creator_location_created": "",
        "creator_identifier": "",
        "creator_facebook_follow": "",
        "creator_facebook_subscribe": "",
        "creator_twitter_follow": "",
        "creator_youtube_subscribe": "",
        "creator_create_video": "",
        "creator_name": "",
        "creator_url": "",
        "facebook_comment": "",
        "facebook_like": "",
        "facebook_share": "",
        "pinterest_share": "",
        "twitter_share": "",
        "tiktok_share": "",
        "tiktok_comment": "",
        "reddit_engagement": "",
        "youtube_watch": "",
        "youtube_comment": "",
        "youtube_like": "",
        "youtube_favorite": "",
        "youtube_subscribe": "",
        "create_video": "",
    },
    {
        "target_url": "https://www.github/medialab/minall",
        "url": "https://www.github/medialab/minall",
        "domain": "",
        "work_type": "",
        "duration": "",
        "identifier": "",
        "date_published": "",
        "date_modified": "",
        "country_of_origin": "",
        "abstract": "",
        "keywords": "",
        "title": "",
        "text": "",
        "hashtags": "",
        "creator_type": "",
        "creator_date_created": "",
        "creator_location_created": "",
        "creator_identifier": "",
        "creator_facebook_follow": "",
        "creator_facebook_subscribe": "",
        "creator_twitter_follow": "",
        "creator_youtube_subscribe": "",
        "creator_create_video": "",
        "creator_name": "",
        "creator_url": "",
        "facebook_comment": "",
        "facebook_like": "",
        "facebook_share": "",
        "pinterest_share": "",
        "twitter_share": "",
        "tiktok_share": "",
        "tiktok_comment": "",
        "reddit_engagement": "",
        "youtube_watch": "",
        "youtube_comment": "",
        "youtube_like": "",
        "youtube_favorite": "",
        "youtube_subscribe": "",
        "create_video": "",
    },
]


if __name__ == "__main__":
    unittest.main()
