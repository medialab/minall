# minall/enrichment/article_text/scraper.py

"""Class and helper function for scraping HTML.

This module's `Scraper` class enhances minet's `request()` and `extract()` methods by providing additional support for unexpected HTML encodings.

1. Uses minet's `request()` method on a target URL to get a `Response` object.
2. Verifies that the `Response` object is encoded in some form of utf-8.
3. Extracts the HTML body from the `Response`. [```text = response.text()```]
4. Uses bs4's fool-proof `UnicodeDammit` to parse the exact encoding. [```UnicodeDammit(text, "html.parser").declared_html_encoding```]
5. Gives the encoding to bs4's `BeautifulSoup` to parse the HTML.
6. Gives the `BeautifulSoup` result to minet's `extract()` method in order to return minet's `TrafilaturaResult` object.

"""

import logging
from typing import Tuple

from bs4 import BeautifulSoup, UnicodeDammit  # type: ignore
from minet.extraction import TrafilaturaResult, extract
from minet.web import Response, request
from rich.progress import Progress

from minall.enrichment import logger


class Scraper:
    """Class to manage HTML scraping.

    Examples:
        >>> scraper = Scraper()
        >>> url, result = scraper(url='https://zenodo.org/records/7974793')
        >>> url == result.canonical_url
        True
        >>> result.title
        'Minet, a webmining CLI tool & library for python.'
    """

    def __init__(
        self, progress: Progress | None = None, total: int | None = None
    ) -> None:
        """If provided the context of a rich progress bar, save it to the class instance and add the task 'Scraping webpage'.

        Args:
            progress (Progress | None, optional): Context of a rich progress bar instance. Defaults to None.
            total (int | None, optional): Total number of items treated during progress context. Defaults to None.
        """
        self.progress = progress
        if progress:
            self.progress = progress
            t = progress.add_task(
                description="[bold yellow]Scraping webpage", total=total
            )
            self.task_id = t

    def __call__(self, url: str) -> Tuple[str, TrafilaturaResult | None]:
        """Requests and scrapes HTML, returning minet's Trafilatura Result object.

        Args:
            url (str): Target URL.

        Returns:
            Tuple[str, TrafilaturaResult | None]: The target URL and, if scraping was successful, minet's Trafilatura Result object.
        """
        if self.progress:
            self.progress.advance(self.task_id)
        result = None
        response = None

        # Request URL's HTML
        try:
            response = request(url)
        except Exception as e:
            logging.error(e)

        # Parse requested HTML
        if response and good_response(response):
            text = response.text()
            try:
                # Avoid input conversion error, deriving from inside Trafilatura's lxml dependency
                encoding = UnicodeDammit(text, "html.parser").declared_html_encoding
                soup = BeautifulSoup(text, features="lxml", from_encoding=encoding)
                text = soup.decode(formatter="html")
                result = extract(text)
            except Exception as e:
                logger.exception(e)
        return url, result


def good_response(response: Response) -> Response | None:
    """Verifies that the response that minet's request method returned is valid for scraping.

    Args:
        response (Response): Response object returned from minet's request method.

    Returns:
        Response | None: If valid, the Response; otherwise None.
    """
    if (
        response.is_text
        and response.encoding
        and "utf" in response.encoding
        and "8" in response.encoding
    ):
        return response
