# minall/enrichment/crowdtangle/contexts.py

"""Context manager for CrowdTangle's CSV writers, multi-threader, and progress bar.
"""

import csv
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
from minall.tables.shared_content import ShareContentConstants


class ContextManager:
    def __init__(self, links_file: Path, shared_content_file: Path):
        """Set up class for scraper's contexts.

        Args:
            links_file (Path): Path to CSV file for post metadata.
            shared_content_file (Path): Path to CSV file for posts' shared content metadata.
        """
        self.links_file = links_file
        self.shared_content_file = shared_content_file

    def __enter__(self) -> Tuple[csv.DictWriter, csv.DictWriter, Progress]:
        """Start the module's context variables.

        Returns:
            Tuple[csv.DictWriter, csv.DictWriter, Progress]: CSV writer for post metadata, CSV writer for shared content metadata, rich progress bar.
        """
        # Set up links file writer
        self.links_file_obj = open(self.links_file, mode="w")
        self.links_file_writer = csv.DictWriter(
            self.links_file_obj, fieldnames=LinksConstants.col_names
        )
        self.links_file_writer.writeheader()

        # Set up shared_content file writer
        self.shared_content_obj = open(self.shared_content_file, mode="w")
        self.shared_content_writer = csv.DictWriter(
            self.shared_content_obj, fieldnames=ShareContentConstants.col_names
        )
        self.shared_content_writer.writeheader()

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
            self.shared_content_writer,
            self.progress_bar,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the scraper's context variables."""
        if self.shared_content_obj:
            self.shared_content_obj.close()
        if self.links_file_obj:
            self.links_file_obj.close()
        self.progress_bar.stop()
