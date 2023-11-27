import unittest
from collections import Counter

from ebbe import Timer
from rich.progress import track

from minall.enrichment.crowdtangle.get_data import parse_rate_limit, yield_facebook_data
from minall.utils.parse_config import APIKeys
from tests.base import BaseTest

POST = ["https://www.facebook.com/100063820962754/posts/721047780032581"]


class CTest(BaseTest):
    def setUp(self) -> None:
        keys = APIKeys(self.config)
        token = keys.crowdtangle_token
        assert token
        self.token = token
        rate_limit = keys.crowdtangle_rate_limit
        rate_limit = parse_rate_limit(rate_limit)
        self.rate_limit = rate_limit

    def test_video(self):
        data = POST

        for url, response in yield_facebook_data(
            data=data, token=self.token, rate_limit=self.rate_limit
        ):
            self.assertIsNotNone(url)
            self.assertIsNotNone(response)

    def test_batch(self):
        data = [POST[0] for _ in range(200)]
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
        self.assertEqual(counter.total(), 200)


if __name__ == "__main__":
    unittest.main()
##
##
