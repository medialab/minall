# minall/enrichment/crowdtangle/get_data.py

"""Module contains functions for collecting, normalizing, and writing data from CrowdTangle.
"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Generator, List, Tuple

from minall.enrichment.crowdtangle.client import CTClient, parse_rate_limit
from minall.enrichment.crowdtangle.contexts import ContextManager
from minall.enrichment.crowdtangle.normalizer import (
    parse_facebook_post,
    parse_shared_content,
)


def get_facebook_post_data(
    data: List[str],
    token: str,
    rate_limit: int | str | None,
    links_outfile: Path,
    shared_content_outfile: Path,
):
    """Function to collect, normalize, and write data from CrowdTangle.

    Args:
        data (List[str]): Set of target Facebook URLs.
        token (str): CrowdTangle API token.
        rate_limit (int | str | None): CrowdTangle API rate limit.
        links_outfile (Path): Path to CSV file for Facebook post metadata.
        shared_content_outfile (Path): Path to CSV for shared content metadata.
    """

    rate_limit = parse_rate_limit(rate_limit)

    with ContextManager(links_outfile, shared_content_outfile) as contexts:
        links_writer, shared_content_writer, progress = contexts

        t = progress.add_task(
            description="[bold blue]Querying Facebook posts", total=len(data)
        )
        for url, response in yield_facebook_data(
            data=data, token=token, rate_limit=rate_limit
        ):
            progress.advance(t)
            formatted_post = parse_facebook_post(url=url, result=response)
            links_writer.writerow(formatted_post)
            for formatted_media in parse_shared_content(url=url, result=response):
                shared_content_writer.writerow(formatted_media)


def yield_facebook_data(
    data: List[str], token: str, rate_limit: int
) -> Generator[Tuple[str, Any], None, None]:
    """Streams target Facebook URLs to multi-threading context and yields minet's results.

    Args:
        data (List[str]): Set of target Facebook URLs.
        token (str): CrowdTangle API token.
        rate_limit (int): CrowdTangle API rate limit.

    Yields:
        Generator[Tuple[str, CrowdTanglePost | None], None, None]: Target Facebook URL and, if available, result of minet's CrowdTangle API client.
    """
    client = CTClient(token=token, rate_limit=rate_limit)
    with ThreadPoolExecutor() as executor:
        for url, response in executor.map(client, data):
            yield url, response
