import logging

import trafilatura
from minet.extraction import TrafilaturaResult
from trafilatura.settings import use_config

logging.basicConfig(filename="trafilatura.log", encoding="utf-8", level=logging.DEBUG)
trafilatura_config = use_config()
trafilatura_config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")


def scraper(url: str) -> tuple[str, TrafilaturaResult | None]:
    result = None
    try:
        downloaded = trafilatura.fetch_url(url)
        extraction = trafilatura.bare_extraction(downloaded)
        if extraction:
            result = TrafilaturaResult.from_bare_extraction(extraction)

    except Exception as e:
        logging.exception(e)

    return url, result
