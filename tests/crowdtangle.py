import unittest

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


if __name__ == "__main__":
    unittest.main()
