# minall/utils/progress_bar.py

"""Context for rich progress bar.
"""

from contextlib import contextmanager
from typing import Generator

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


@contextmanager
def progress_bar() -> Generator[Progress, None, None]:
    """Rich progress bar with Spinner column.

    Yields:
        Generator[Progress, None, None]: Rich progress bar context
    """
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        yield progress
