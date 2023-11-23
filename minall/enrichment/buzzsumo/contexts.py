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


class WriterContext:
    def __init__(self, links_file: Path):
        self.links_file = links_file

    def __enter__(self):
        # Set up links file writer
        self.links_file_obj = open(self.links_file, mode="w")
        self.links_file_writer = csv.DictWriter(
            self.links_file_obj, fieldnames=LinksConstants.col_names
        )
        self.links_file_writer.writeheader()

        return self.links_file_writer

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.links_file_obj:
            self.links_file_obj.close()


class GeneratorContext:
    def __init__(self) -> None:
        pass

    def __enter__(self):
        # Set up progress bar
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
        self.progress_bar.stop()
        self.executor.shutdown(wait=False, cancel_futures=True)
