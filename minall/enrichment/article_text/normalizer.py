# minall/enrichment/article_text/constants.py

"""Dataclass to normlalize minet's Trafilatura result object.
"""

from dataclasses import dataclass

from casanova import TabularRecord
from minet.extraction import TrafilaturaResult


@dataclass
class NormalizedScrapedWebPage(TabularRecord):
    """Dataclass to normlalize minet's Trafilatura result object.

    Attributes:
        url (str): URL targeted for scraping.
        title (str | None): Title scraped from HTML.
        text (str | None): Main text scraped from HTML.
        date_published (str | None): Date scraped from HTML.
        work_type (str): Target URL's schema subtype. Default = "WebPage".
    """

    url: str
    title: str | None
    text: str | None
    date_published: str | None
    work_type: str = "WebPage"

    @classmethod
    def from_payload(
        cls,
        url: str,
        result: TrafilaturaResult,
    ) -> "NormalizedScrapedWebPage":
        return NormalizedScrapedWebPage(
            url=url, title=result.title, text=result.content, date_published=result.date
        )
