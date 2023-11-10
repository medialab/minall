from pathlib import Path

from minall.enrichment.article_text.constants import NormalizedScrapedWebPage
from minall.enrichment.article_text.contexts import ContextManager
from minall.enrichment.article_text.scraper import scraper


def get_data(data: list[tuple[str, str]], outfile: Path):
    with ContextManager(links_file=outfile) as contexts:
        writer, executor, progress = contexts
        t = progress.add_task(
            description="[bold yellow]Scraping webpage", total=len(data)
        )
        for url, result in executor.map(scraper, data):
            if result:
                formatted_result = NormalizedScrapedWebPage.from_payload(
                    url=url, result=result
                )
                writer.writerow(formatted_result.as_csv_dict_row())
            progress.advance(t)
