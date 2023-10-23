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

from minall.enrichment.crowdtangle.constants import CrowdTangleResult

logging.basicConfig(filename="crowdtangle.log", encoding="utf-8")


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

    def __call__(self, data: tuple[str, str]) -> CrowdTangleResult:
        # Parse the incoming tuple of data
        url = data[0]
        link_id = data[1]
        result = CrowdTangleResult()
        post_id = None

        # Attempt to parse the post's ID
        try:
            post_id = facebook.post_id_from_url(url)
        except Exception as error:
            msg = (
                "\n\n"
                "Unable to parse the post ID from url: {url}\n"
                "Encountered error: {error}".format(url=url, error=error)
            )
            logging.warning(msg)

        if post_id is not None:
            # Attempt to collect the post's data
            try:
                post = self.client.post(post_id=post_id)
                if post is not None:
                    result = CrowdTangleResult(
                        link_id=link_id, url=url, FacebookPost=post
                    )
            except CrowdTanglePostNotFound as error:
                msg = (
                    "\n\n"
                    "CrowdTangle does not have data about the post at this url: {url}\n"
                    "The CrowdTangle API's response is: \n{data}\n".format(
                        url=url, data=error.data
                    )
                )
                logging.warning(msg)
        return result
