# minall/enrichment/youtube/context.py

"""Module containing contexts for YouTube data collection's CSV writer and progress bar.
"""

import csv
from pathlib import Path

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from minall.tables.links import LinksConstants


class ProgressBar:
    """Context for rich progress bar."""

    def __init__(self) -> None:
        pass

    def __enter__(self) -> Progress:
        """Start the rich progress bar.

        Returns:
            Progress: Context variable for rich progress bar.
        """

        self.progress_bar = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )
        self.progress_bar.start()
        return self.progress_bar

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stops the progress bar's context variable."""
        self.progress_bar.stop()


class Writer:
    """Context for writing YouTube links metadata to CSV of 'links' SQL table."""

    def __init__(self, links_file: Path):
        """Set up class for iteratively writing normalized YouTube results to CSV.

        Args:
            links_file (Path): Path to the links table CSV file.
        """
        self.links_file = links_file

    def __enter__(self) -> csv.DictWriter:
        """Start the CSV writer's context.

        Returns:
            csv.DictWriter: Context variable for writing CSV rows.
        """

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
