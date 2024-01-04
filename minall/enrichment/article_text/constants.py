# minall/enrichment/article_text/constants.py

"""Something.
"""

from dataclasses import dataclass

from casanova import TabularRecord
from minet.extraction import TrafilaturaResult


@dataclass
class NormalizedScrapedWebPage(TabularRecord):
    """_summary_

    Attributes:
        url (str): __description__
        title (str | None): __description__
        text (str | None): __description__
        date_published (str | None): __description__
        work_type (str): __description__. Default = "WebPage".
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
