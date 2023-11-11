import logging
from typing import Tuple

from bs4 import UnicodeDammit  # type: ignore
from minet.extraction import TrafilaturaResult, extract
from minet.web import request
from rich.progress import Progress

from minall.enrichment import logger


class Scraper:
    def __init__(self, progress: Progress, total: int) -> None:
        self.progress = progress
        t = progress.add_task(description="[bold yellow]Scraping webpage", total=total)
        self.task_id = t

    def advance(self) -> None:
        self.progress.advance(self.task_id)

    def __call__(self, url: str) -> Tuple[str, TrafilaturaResult | None]:
        self.advance()
        result = None
        response = None

        # Request URL's HTML
        try:
            response = request(url)
        except Exception as e:
            logging.error(e)

        # Parse requested HTML
        if response and response.is_text and response.encoding == "utf_8":
            text = response.text()
            try:
                # Avoid input conversion error, deriving from inside Trafilatura's lxml dependency
                soup = UnicodeDammit(text, "html.parser")
                text = soup.decode(formatter="html")
                result = extract(text)
            except Exception as e:
                logger.exception(e)
        return url, result
