import csv
import unittest
from collections import Counter
from pathlib import Path

from ebbe import Timer
from rich.progress import track

from minall.enrichment.crowdtangle.get_data import (
    get_facebook_post_data,
    parse_rate_limit,
    yield_facebook_data,
)
from minall.utils.parse_config import APIKeys
from tests.base import BaseTest

POST = ["https://www.facebook.com/100063820962754/posts/721047780032581"]

URLS = [
    "https://www.facebook.com/100083914530758/posts/282967607843722",
    "https://www.facebook.com/100063820962754/posts/721047780032581",
    "https://www.facebook.com/100093027842398/posts/113675801743348",
    "https://www.facebook.com/groups/250350359176207/posts/1197754131102487",
    "https://www.facebook.com/100064618422451/posts/577329744430968",
    "https://www.facebook.com/100021536891754/posts/1179475059447046",
    "https://www.facebook.com/100064144775853/posts/497193825762106",
    "https://www.facebook.com/100064044939758/posts/510244237787070",
    "https://www.facebook.com/100081439001139/posts/154151503976149",
    "https://www.facebook.com/100063975222705/posts/457396283069542",
    "https://www.facebook.com/groups/296568575193397/posts/455627409287512/",
    "https://www.facebook.com/115241179889331/posts/760261572053952",
    "https://www.facebook.com/groups/358688005931897/posts/537408748059821/",
    "https://www.facebook.com/842597032524957/posts/4624922730959016",
    "https://www.facebook.com/permalink.php?story_fbid=441808253971964&id=100044283797100",
    "https://www.facebook.com/groups/960617117610735/permalink/1544671352538639/",
    "https://www.facebook.com/permalink.php?story_fbid=4590570124322043&id=1353729974672757",
    "https://www.facebook.com/100057337034462/posts/376736994247532",
    "https://www.facebook.com/permalink.php?story_fbid=262267762531315&id=106582174766542",
    "https://www.facebook.com/185368328214055/posts/4544903955593782",
    "https://www.facebook.com/435962897166227/posts/1064892704273240",
    "https://www.facebook.com/53638966652/posts/10158122097671653",
]


class CTest(BaseTest):
    links_outfile = Path(__file__).parent.joinpath("links.csv")
    shared_content_outfile = Path(__file__).parent.joinpath("shared_content.csv")

    def setUp(self) -> None:
        keys = APIKeys(self.config)
        token = keys.crowdtangle_token
        assert token
        self.token = token
        rate_limit = keys.crowdtangle_rate_limit
        rate_limit = parse_rate_limit(rate_limit)
        self.rate_limit = rate_limit

    def test(self):
        get_facebook_post_data(
            data=URLS,
            token=self.token,
            rate_limit=self.rate_limit,
            links_outfile=self.links_outfile,
            shared_content_outfile=self.shared_content_outfile,
        )
        with open(self.links_outfile) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.assertEqual(row["domain"], "facebook.com")
                self.assertNotEqual(row["text"], "")

    @unittest.skip("")
    def test_video(self):
        data = POST

        for url, response in yield_facebook_data(
            data=data, token=self.token, rate_limit=self.rate_limit
        ):
            self.assertIsNotNone(url)
            self.assertIsNotNone(response)

    @unittest.skip("")
    def test_batch(self):
        BATCH = 200
        data = [POST[0] for _ in range(BATCH)]
        counter = Counter()
        with Timer(name=f"CT batch {len(data)}"):
            for url, response in track(
                yield_facebook_data(
                    data=data, token=self.token, rate_limit=self.rate_limit
                ),
                total=len(data),
            ):
                if response:
                    self.assertEqual(getattr(response, "platform"), "Facebook")
                    counter.update([url])
        self.assertEqual(counter.total(), BATCH)

    def tearDown(self):
        Path.unlink(self.links_outfile)
        Path.unlink(self.shared_content_outfile)


if __name__ == "__main__":
    unittest.main()
