# minall/enrichment/article_text/contexts.py

"""Something.
"""

import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from minall.tables.links.constants import LinksConstants


class ContextManager:
    def __init__(self, links_file: Path):
        self.links_file = links_file

    def __enter__(self):
        # Set up links file writer
        self.links_file_obj = open(self.links_file, mode="w", encoding="utf-8")
        self.links_file_writer = csv.DictWriter(
            self.links_file_obj, fieldnames=LinksConstants.col_names
        )
        self.links_file_writer.writeheader()

        # Set up multi-threading pool
        self.executor = ThreadPoolExecutor(max_workers=3)

        # Set up progress bar
        self.progress_bar = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )
        self.progress_bar.start()

        return (
            self.links_file_writer,
            self.executor,
            self.progress_bar,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.links_file_obj:
            self.links_file_obj.close()
        self.executor.shutdown(wait=False, cancel_futures=True)
        self.progress_bar.stop()
