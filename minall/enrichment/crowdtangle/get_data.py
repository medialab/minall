import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from minall.enrichment.crowdtangle.client import FacebookPostCommand
from minall.enrichment.crowdtangle.normalizer import ResultParser
from minall.links.constants import LINKS_FIELDNAMES
from minall.shared_content.constants import SHARED_CONTENT_FIELDNAMES
from minall.utils import progress_bar


def get_facebook_post_data(
    data: list[tuple[str, str]],
    token: str,
    rate_limit: int,
    appearances_outfile: Path,
    shared_content_outfile: Path,
):
    with ThreadPoolExecutor() as executor, progress_bar() as progress, open(
        appearances_outfile, "w"
    ) as aof, open(shared_content_outfile, "w") as scof:
        # Set up CSV writers
        links_writer = csv.DictWriter(aof, fieldnames=LINKS_FIELDNAMES)
        links_writer.writeheader()
        shared_content_writer = csv.DictWriter(
            scof, fieldnames=SHARED_CONTENT_FIELDNAMES
        )
        shared_content_writer.writeheader()

        # Set up minet's CrowdTangle API client
        client = FacebookPostCommand(token=token, rate_limit=rate_limit)

        # Set up normalizers for minet's response
        result_parser = ResultParser(
            links_writer=links_writer,
            shared_content_writer=shared_content_writer,
        )

        # Set up the progress bar
        t = progress.add_task(description="[blue]Facebook", total=len(data))

        print(
            f"\n\tWriting Facebook results to files '{appearances_outfile}' and '{shared_content_outfile}'"
        )
        for result in executor.map(client, data):
            # Parse the results and write to 2 different CSVs
            result_parser(result)
            progress.advance(t)
