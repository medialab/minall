# minall/enrichment/article_text/get_data.py

"""Module contains a function that runs the scraping feature.
"""

from pathlib import Path

from minall.enrichment.article_text.contexts import ContextManager
from minall.enrichment.article_text.normalizer import NormalizedScrapedWebPage
from minall.enrichment.article_text.scraper import Scraper


def get_data(data: list[str], outfile: Path):
    """Iterating through the target URLs, scrape data and write to out-file.

    Args:
        data (list[str]): Set of target URLs for scraping.
        outfile (Path): Path to CSV file for writing normalized results.
    """
    with ContextManager(links_file=outfile) as contexts:
        writer, executor, progress = contexts
        scraper = Scraper(progress=progress, total=len(data))
        for url, result in executor.map(scraper, data):
            if result:
                formatted_result = NormalizedScrapedWebPage.from_payload(
                    url=url, result=result
                )
                writer.writerow(formatted_result.as_csv_dict_row())
