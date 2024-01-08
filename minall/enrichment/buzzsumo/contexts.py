# minall/enrichment/buzzsumo/contexts.py

"""Module containing contexts for Buzzsumo data collection's CSV writer, progress bar, and multi-threader.
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


class WriterContext:
    def __init__(self, links_file: Path):
        """Set up class for iteratively writing normalized Buzzsumo results to CSV.

        Args:
            links_file (Path): Path to the links table CSV file.
        """
        self.links_file = links_file

    def __enter__(self) -> csv.DictWriter:
        """Start the CSV writer's context.

        Returns:
            csv.DictWriter: Context variable for writing CSV rows.
        """
        # Set up links file writer
        self.links_file_obj = open(self.links_file, mode="w")
        self.links_file_writer = csv.DictWriter(
            self.links_file_obj, fieldnames=LinksConstants.col_names
        )
        self.links_file_writer.writeheader()

        return self.links_file_writer

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stops the writer's context variable."""
        if self.links_file_obj:
            self.links_file_obj.close()


class GeneratorContext:
    def __init__(self) -> None:
        """Set up class for Buzzsumo client wrapper's contexts."""
        pass

    def __enter__(self) -> Tuple[Progress, ThreadPoolExecutor]:
        """Start the wrapper's context variables.

        Returns:
            Tuple[Progress, ThreadPoolExecutor]: Context variables.
        """
        self.progress_bar = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )
        self.progress_bar.start()

        self.executor = ThreadPoolExecutor()

        return self.progress_bar, self.executor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the Buzzsumo client wrapper's context variables."""
        self.progress_bar.stop()
        self.executor.shutdown(wait=False, cancel_futures=True)
