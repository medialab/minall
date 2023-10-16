import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from minet.buzzsumo.client import BuzzSumoAPIClient

from minall.enrichment.buzzsumo.constants import BEGINDATE, ENDDATE, BuzzsumoResult
from minall.enrichment.buzzsumo.normalizer import BuzzsumoNormalizer
from minall.links.constants import LINKS_FIELDNAMES
from minall.utils import progress_bar


def get_buzzsumo_data(data: list[tuple[str, str]], token: str, outfile: Path):
    with ThreadPoolExecutor() as executor, open(outfile, "w") as of:
        # Set up the CSV in which to store the collected metadata
        writer = csv.DictWriter(of, fieldnames=LINKS_FIELDNAMES)
        writer.writeheader()

        # Set up minet's Buzzsumo API client
        client = BuzzsumoCommand(token=token)

        # Set up a normalizer to reformat minet's data according to the destination,
        # either the appearances table or reviews table
        normalizer = BuzzsumoNormalizer(fields=LINKS_FIELDNAMES)

        # Set up the progress bar's task

        # With a multithreader, collect and output Buzzsumo data to a CSV file
        print(f"\n\tWriting Buzzsumo results to '{outfile}'")
        with progress_bar() as progress:
            t = progress.add_task("[green]Buzzsumo", total=len(data))
            for result in executor.map(client, data):
                normalized_result = normalizer(
                    url=result.url, link_id=result.link_id, data=result._asdict()
                )
                writer.writerow(normalized_result)
                progress.advance(t)


class BuzzsumoCommand:
    def __init__(self, token: str) -> None:
        self.client = BuzzSumoAPIClient(token=token)
        self.begin_date = BEGINDATE
        self.end_date = ENDDATE

    def __call__(self, data: tuple[str, str]) -> BuzzsumoResult:
        # Parse the incoming tuple of data
        url = data[0]
        link_id = data[1]

        # Call minet's Buzzsumo client method
        result = self.client.exact_url(
            search_url=url, begin_timestamp=self.begin_date, end_timestamp=self.end_date
        )

        # Return a named tuple of the desired information
        return BuzzsumoResult(link_id=link_id, url=url, BuzzsumoExactURL=result)
