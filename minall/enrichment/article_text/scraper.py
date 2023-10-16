import logging

import trafilatura
from minet.extraction import TrafilaturaResult
from trafilatura.settings import use_config

from minall.enrichment.article_text.normalizer import ArticleNormalizer

logging.basicConfig(filename="trafilatura.log", encoding="utf-8", level=logging.DEBUG)
trafilatura_config = use_config()
trafilatura_config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")


class ArticleScraper:
    def __init__(self) -> None:
        self.normalizer = ArticleNormalizer()

    def __call__(self, data: tuple[str, str]) -> dict:
        final_output = {}

        url = data[0]
        link_id = data[1]

        try:
            downloaded = trafilatura.fetch_url(url)
            extraction = trafilatura.bare_extraction(downloaded)
            if extraction:
                result = TrafilaturaResult.from_bare_extraction(extraction)
                final_output = self.normalizer(result, url, link_id)

        except Exception as e:
            logging.exception(e)

        return final_output
