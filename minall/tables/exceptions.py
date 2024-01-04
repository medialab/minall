# minall/exceptions.py

"""Exceptions for validating CSV files used to create SQLite tables.

This module contains exceptions to manage the process of validating a CSV file given as input for the enrichment process. The module contains the following exceptions:

- `NoCSVHeaders` - The CSV does not have headers.
- `NoURLColumn` - When building the 'links' table, the declared URL column is not in the CSV file.
- `NoPrimaryKeyColumns` - When building the 'shared_content' table, either the 'post_url' column or the 'content_url' column are missing from the CSV file.

When creating the 'links' table, the input CSV file must have a column for URLs; the URLs must be cleaned and/or ready to serve as the source for the data collection. The name of the URL column can vary and must be declared.

When creating the 'shared_content' table, the column names are not modifiable. The CSV must have the columns 'post_url' and 'content_url;' the former relates to a URL in the 'links' table, and the latter incidates a URL for content embedded in the Web Content of the former.
"""


class NoCSVHeaders(Exception):
    """The CSV in-file lacks headers."""

    def __init__(self) -> None:
        message = "No headers detected in CSV file."
        super().__init__(message)


class NoURLColumn(Exception):
    """The CSV in-file is missing a user-declared column."""

    def __init__(self, url_col: str) -> None:
        message = f"The declared URL column '{url_col}' is not a header in the given CSV file."
        super().__init__(message)


class NoPrimaryKeyColumns(Exception):
    """The CSV in-file is missing a required column."""

    def __init__(self, col: str) -> None:
        message = f"Required primary key column '{col}' is not a header in the given CSV file."
        super().__init__(message)
