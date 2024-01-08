# minall/enrichment/article_text/contexts.py

"""Context manager for scraper's CSV writers, multi-threader, and progress bar.
"""

import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Tuple

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from minall.tables.links import LinksConstants


class ContextManager:
    def __init__(self, links_file: Path):
        """Set up class for scraper's contexts.

        Args:
            links_file (Path): Path to out-file for CSV writer.
        """
        self.links_file = links_file

    def __enter__(self) -> Tuple[csv.DictWriter, ThreadPoolExecutor, Progress]:
        """Start the scraper's context variables.

        Returns:
            Tuple[csv.DictWriter, ThreadPoolExecutor, Progress]: Context variables.
        """
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
        """Stop the scraper's context variables."""
        if self.links_file_obj:
            self.links_file_obj.close()
        self.executor.shutdown(wait=False, cancel_futures=True)
        self.progress_bar.stop()
