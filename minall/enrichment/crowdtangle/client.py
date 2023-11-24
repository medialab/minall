import logging

from minet.crowdtangle.client import CrowdTangleAPIClient
from minet.facebook import post_id_from_url
from ural.facebook import parse_facebook_url


def parse_rate_limit(rate_limit):
    if not rate_limit:
        rate_limit = 10
    elif isinstance(rate_limit, str):
        rate_limit = int(rate_limit)
    return rate_limit


def adhoc_post_id_parser(url: str):
    post_id = post_id_from_url(url)
    if post_id:
        return post_id
    else:
        parsed_url = parse_facebook_url(url)
        if parsed_url:
            if hasattr(parsed_url, "id"):
                post_id = getattr(parsed_url, "id")
            else:
                return
            if hasattr(parsed_url, "parent_handle"):
                parent_id = getattr(parsed_url, "parent_handle")
            elif hasattr(parsed_url, "parent_id"):
                parent_id = getattr(parsed_url, "parent_id")
            else:
                return
            if post_id and parent_id:
                try:
                    int(post_id)
                except Exception:
                    return
                try:
                    int(parent_id)
                except Exception:
                    return
                return post_id + "_" + parent_id


class CTClient:
    def __init__(self, token: str, rate_limit: int) -> None:
        self.client = CrowdTangleAPIClient(token=token, rate_limit=rate_limit)

    def __call__(self, url: str):
        post_id = adhoc_post_id_parser(url)
        post = None
        if post_id:
            try:
                post = self.client.post(post_id=post_id)
            except Exception as e:
                logging.exception(e)
        return post
