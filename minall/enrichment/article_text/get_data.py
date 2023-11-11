from pathlib import Path

from minall.enrichment.article_text.constants import NormalizedScrapedWebPage
from minall.enrichment.article_text.contexts import ContextManager
from minall.enrichment.article_text.scraper import Scraper


def get_data(data: list[str], outfile: Path):
    with ContextManager(links_file=outfile) as contexts:
        writer, executor, progress = contexts
        scraper = Scraper(progress=progress, total=len(data))
        for url, result in executor.map(scraper, data):
            if result:
                formatted_result = NormalizedScrapedWebPage.from_payload(
                    url=url, result=result
                )
                writer.writerow(formatted_result.as_csv_dict_row())
