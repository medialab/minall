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
from minall.tables.shared_content import ShareContentConstants


class ContextManager:
    def __init__(self, links_file: Path, shared_content_file: Path):
        self.links_file = links_file
        self.shared_content_file = shared_content_file

    def __enter__(self):
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
        if self.shared_content_obj:
            self.shared_content_obj.close()
        if self.links_file_obj:
            self.links_file_obj.close()
        self.progress_bar.stop()
