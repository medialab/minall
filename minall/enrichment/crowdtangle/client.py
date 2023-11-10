import logging

import minet.facebook as facebook
from minet.crowdtangle.client import CrowdTangleAPIClient
from minet.crowdtangle.exceptions import (
    CrowdTangleInvalidJSONError,
    CrowdTanglePostNotFound,
    CrowdTangleRateLimitExceeded,
    CrowdTangleServerError,
)
from minet.web import create_request_retryer

from minall.enrichment.crowdtangle.exceptions import NoPostID, PostNotFound

logging.basicConfig(filename="crowdtangle.log", encoding="utf-8")


def parse_rate_limit(rate_limit):
    if not rate_limit:
        rate_limit = 10
    elif isinstance(rate_limit, str):
        rate_limit = int(rate_limit)
    return rate_limit


class FacebookPostCommand:
    def __init__(self, token: str, rate_limit: int) -> None:
        self.client = CrowdTangleAPIClient(token=token, rate_limit=rate_limit)
        self.client.retryer = create_request_retryer(
            additional_exceptions=[
                CrowdTangleRateLimitExceeded,
                CrowdTangleInvalidJSONError,
                CrowdTangleServerError,
            ]
        )

    def __call__(self, url: str) -> tuple:
        # Parse the incoming tuple of data
        post_id = None
        result = None

        # Attempt to parse the post's ID
        try:
            post_id = facebook.post_id_from_url(url)
        except Exception as error:
            logging.warning(NoPostID(error, url))

        if post_id is not None:
            # Attempt to collect the post's data
            try:
                post = self.client.post(post_id=post_id)
                if post is not None:
                    result = post
            except CrowdTanglePostNotFound as error:
                logging.warning(PostNotFound(url, error))
        return (url, result)
