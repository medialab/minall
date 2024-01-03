# minall/exceptions.py

"""Tools to validate CSV file used for creating SQLite table.

This module contains a function and exceptions to manage the process of validating a CSV file given as the URL dataset for the enrichment process. The function is called when one of the SQLite's tables are being created. The module contains the following function and exceptions:

- `check_csv_headers(table_name, infile_path, url_col)` - Parse columns in CSV file and raise exception if invalid.
- `NoCSVHeaders` - The CSV does not have headers.
- `NoURLColumn` - When building the 'links' table, the declared URL column is not in the CSV file.
- `NoPrimaryKeyColumns` - When building the 'shared_content' table, either the 'post_url' column or the 'content_url' column are missing from the CSV file.

When creating the 'links' table, the input CSV file must have a column for URLs; the URLs must be cleaned and/or ready to serve as the source for the data collection. The name of the URL column can vary and must be declared.

When creating the 'shared_content' table, the column names are not modifiable. The CSV must have the columns 'post_url' and 'content_url;' the former relates to a URL in the 'links' table, and the latter incidates a URL for content embedded in the Web Content of the former.
"""

from typing import List

import casanova


def check_csv_headers(
    table_name: str, infile_path: str, url_col: str | None
) -> List[str]:
    """_summary_

    Args:
        table_name (str): _description_
        infile_path (str): _description_
        url_col (str | None): _description_

    Raises:
        NoCSVHeaders: _description_
        NoURLColumn: _description_
        NoPrimaryKeyColumns: _description_

    Returns:
        List[str]: _description_
    """
    with casanova.reader(infile_path) as reader:
        columns = reader.fieldnames

    if not isinstance(columns, List):
        raise NoCSVHeaders()

    if table_name == "links":
        if url_col not in columns:
            raise NoURLColumn(str(url_col))

    elif table_name == "shared_content":
        if "post_url" not in columns:
            raise NoPrimaryKeyColumns("post_url")
        if "content_url" not in columns:
            raise NoPrimaryKeyColumns("content_url")
    return columns


class NoCSVHeaders(Exception):
    def __init__(self) -> None:
        # Call the base class constructor with the parameters it needs
        message = "No headers detected in CSV file."
        super().__init__(message)


class NoURLColumn(Exception):
    def __init__(self, url_col: str) -> None:
        # Call the base class constructor with the parameters it needs
        message = f"The declared URL column '{url_col}' is not a header in the given CSV file."
        super().__init__(message)


class NoPrimaryKeyColumns(Exception):
    def __init__(self, col: str) -> None:
        # Call the base class constructor with the parameters it needs
        message = f"Required primary key column '{col}' is not a header in the given CSV file."
        super().__init__(message)
