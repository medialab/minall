from pathlib import Path
from typing import Generator, List

from minet.buzzsumo.client import BuzzSumoAPIClient

from minall.enrichment.buzzsumo.constants import (
    BEGINDATE,
    ENDDATE,
    NormalizedBuzzsumoResult,
)
from minall.enrichment.buzzsumo.contexts import ContextManager


def get_buzzsumo_data(data: List[str], token: str, outfile: Path):
    """Main function for writing Buzzsumo API results to a CSV file.

    Args:
        data (List[str]): List of URLs.
        token (str): Token for Buzzsumo API.
        outfile (Path): Path to CSV file in which to write results.
    """
    with ContextManager(links_file=outfile) as contexts:
        writer, progress = contexts
        t = progress.add_task("[green]Calling Buzzsumo API", total=len(data))
        for formatted_result in yield_buzzsumo_data(token=token, data=data):
            writer.writerow(formatted_result.as_csv_dict_row())
            progress.advance(t)


def yield_buzzsumo_data(
    token: str, data: List[str]
) -> Generator[NormalizedBuzzsumoResult, None, None]:
    """Call Buzzsumo API and yield normalized data. Rely on single-threaded requests
    in order to manage Buzzsumo API's rate limit of 10 calls in every 10-second window.

    Args:
        token (str): Token for Buzzsumo API.
        data (List[str]): List of URLs.

    Yields:
        Generator[NormalizedBuzzsumoResult, None, None]: API result formatted in dataclass.
    """
    # Set up minet's Buzzsumo API client
    client = BuzzSumoAPIClient(token=token)

    for url in data:
        result = client.exact_url(
            search_url=url, begin_timestamp=BEGINDATE, end_timestamp=ENDDATE
        )
        yield NormalizedBuzzsumoResult.from_payload(url, result)
