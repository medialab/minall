# minall/enrichment/crowdtangle/client.py

"""Module contains a client and helper functions for collecting data from CrowdTangle.
"""

import logging
from typing import Tuple

from minet.crowdtangle.client import CrowdTangleAPIClient
from minet.crowdtangle.types import CrowdTanglePost
from minet.facebook import post_id_from_url
from ural.facebook import parse_facebook_url


def parse_rate_limit(rate_limit: int | str | None) -> int:
    """Set default or convert rate limit string to integer.

    Args:
        rate_limit (int | str | None): Value of rate limit for CrowdTangle API.

    Returns:
        int: Converted rate limit integer for CrowdTangle API.
    """
    if not rate_limit:
        rate_limit = 10
    elif isinstance(rate_limit, str):
        rate_limit = int(rate_limit)
    return rate_limit


def adhoc_post_id_parser(url: str) -> str | None:
    """Helper function to catch and fix problems parsing Facebook post ID.

    Args:
        url (str): Target Facebook URL.

    Returns:
        str | None: If successful, post ID for target Facebook URL.
    """
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
    """Wrapper for minet's CrowdTangle API client with helper function for parsing Facebook post ID."""

    def __init__(self, token: str, rate_limit: int) -> None:
        """Create instance of minet's CrowdTangle API client.

        Args:
            token (str): CrowdTangle API token.
            rate_limit (int): CrowdTangle API rate limit.
        """
        self.client = CrowdTangleAPIClient(token=token, rate_limit=rate_limit)

    def __call__(self, url: str) -> Tuple[str, CrowdTanglePost | None]:
        """Execute collection of CrowdTangle data from parsed Facebook post ID.

        Args:
            url (str): Target Facebook URL.

        Returns:
            Tuple[str, CrowdTanglePost | None]: Target URL and, if successful, minet's CrowdTanglePost result object.
        """
        post_id = adhoc_post_id_parser(url)
        post = None
        if post_id:
            try:
                post = self.client.post(post_id=post_id)
            except Exception as e:
                logging.exception(e)
        return url, post
