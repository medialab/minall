import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from minall.enrichment.article_text.scraper import ArticleScraper
from minall.links.constants import LINKS_FIELDNAMES
from minall.utils import progress_bar


def get_data(data: list[tuple[str, str]], outfile: Path):
    scraper = ArticleScraper()

    with ThreadPoolExecutor() as executor, progress_bar() as progress, open(
        outfile, "w"
    ) as of:
        writer = csv.DictWriter(of, fieldnames=LINKS_FIELDNAMES)
        writer.writeheader()
        t = progress.add_task(description="[yellow]Article text", total=len(data))
        for result in executor.map(scraper, data):
            if result != {}:
                writer.writerow(result)
                progress.advance(t)
