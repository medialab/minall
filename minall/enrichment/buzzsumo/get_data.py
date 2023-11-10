from pathlib import Path

from minall.enrichment.buzzsumo.client import BuzzsumoCommand
from minall.enrichment.buzzsumo.constants import NormalizedBuzzsumoResult
from minall.enrichment.buzzsumo.contexts import ContextManager


def get_buzzsumo_data(data: list[str], token: str, outfile: Path):
    with ContextManager(links_file=outfile) as contexts:
        writer, executor, progress = contexts

        # Set up minet's Buzzsumo API client
        client = BuzzsumoCommand(token=token)

        t = progress.add_task("[green]Calling Buzzsumo API", total=len(data))
        for url, result in executor.map(client, data):
            formatted_result = NormalizedBuzzsumoResult.from_payload(url, result)
            writer.writerow(formatted_result.as_csv_dict_row())
            progress.advance(t)
