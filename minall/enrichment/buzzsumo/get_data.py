# minall/enrichment/buzzsumo/get_data.py

"""Module containing a function that runs all of the Buzzsumo enrichment process.
"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Generator, List

from minall.enrichment.buzzsumo.client import BuzzsumoClient
from minall.enrichment.buzzsumo.contexts import GeneratorContext, WriterContext
from minall.enrichment.buzzsumo.normalizer import NormalizedBuzzsumoResult


def get_buzzsumo_data(data: List[str], token: str, outfile: Path):
    """Main function for writing Buzzsumo API results to a CSV file.

    Args:
        data (List[str]): List of URLs.
        token (str): Token for Buzzsumo API.
        outfile (Path): Path to CSV file in which to write results.
    """
    with WriterContext(links_file=outfile) as writer:
        # Save results to memory, trigger Global Interpreter Lock (GIL)
        for result in yield_buzzsumo_data(token, data):
            writer.writerow(result.as_csv_dict_row())


def yield_buzzsumo_data(
    token: str, data: List[str]
) -> Generator[NormalizedBuzzsumoResult, None, None]:
    client = BuzzsumoClient(token=token)

    with GeneratorContext() as context:
        progress, executor = context
        t = progress.add_task("[green]Calling Buzzsumo API", total=len(data))
        for result in executor.map(client, data):
            progress.advance(t)
            yield result
