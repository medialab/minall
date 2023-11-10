from contextlib import contextmanager

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


@contextmanager
def progress_bar():
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        yield progress
