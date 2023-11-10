from dataclasses import dataclass

from casanova import TabularRecord
from minet.extraction import TrafilaturaResult


@dataclass
class NormalizedScrapedWebPage(TabularRecord):
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
