from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from minall.enrichment.buzzsumo.client import BuzzsumoCommand
from minall.enrichment.buzzsumo.constants import NormalizedBuzzsumoResult
from minall.enrichment.buzzsumo.contexts import ContextManager


def get_buzzsumo_data(data: List[str], token: str, outfile: Path):
    with ContextManager(links_file=outfile) as contexts:
        writer, progress = contexts

        # Set up minet's Buzzsumo API client
        t = progress.add_task("[green]Calling Buzzsumo API", total=len(data))
        for formatted_result in yield_buzzsumo_data(token=token, data=data):
            writer.writerow(formatted_result.as_csv_dict_row())
            progress.advance(t)


def yield_buzzsumo_data(token: str, data: List[str]):
    # Set up minet's Buzzsumo API client
    client = BuzzsumoCommand(token=token)

    with ThreadPoolExecutor() as executor:
        for url, result in executor.map(client, data):
            yield NormalizedBuzzsumoResult.from_payload(url, result)
