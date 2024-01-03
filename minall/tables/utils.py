# minall/tables/utils.py

"""Something.

This module contains helper functions and methods used by the SQLite tables.

"""

import csv
from dataclasses import dataclass, field
from sqlite3 import Connection
from typing import Dict, List

from minall.exceptions import check_csv_headers
from minall.tables.links.constants import LinksConstants
from minall.tables.shared_content.constants import ShareContentConstants
from minall.utils.database import SQLiteWrapper


@dataclass
class ColumnParser:
    """_summary_

    Attributes:
        infile_dtype_string (str): __something__
        infile_original (List[str]): __something__
        infile_standardized (List[str]): __something__
        infile_dtypes (Dict): __something__
    """

    infile_dtype_string: str
    infile_original: List[str] = field(default_factory=List)
    infile_standardized: List[str] = field(default_factory=List)
    infile_dtypes: Dict = field(default_factory=Dict)

    def __init__(
        self,
        connection: Connection,
        table_constants: LinksConstants | ShareContentConstants,
        infile: str | None,
        url_col: str | None,
    ):
        """_summary_

        Args:
            connection (Connection): _description_
            table_constants (LinksConstants | ShareContentConstants): _description_
            infile (str | None): _description_
            url_col (str | None): _description_
        """
        self.connection = connection
        self.infile = infile
        self.url_col = url_col
        self.table = table_constants

        self.infile_original = self.parse_original_infile_columns()
        self.infile_standardized = self.standardize_infile_columns()
        self.infile_dtype = self.set_infile_column_dtypes()
        self.infile_dtype_string = ", ".join(
            [f"{col} {dtype}" for col, dtype in self.infile_dtype.items()]
        )

    def parse_original_infile_columns(self) -> List[str]:
        """_summary_

        Raises:
            e: _description_

        Returns:
            List[str]: _description_
        """
        columns = list(self.table.col_names)
        if self.infile:
            try:
                columns = check_csv_headers(
                    self.table.table_name, self.infile, self.url_col
                )
            except Exception as e:
                raise e
        return columns

    def standardize_infile_columns(self) -> List[str]:
        """_summary_

        Returns:
            List[str]: _description_
        """
        # Copy all the columns from the in-file
        standardized_infile_headers = self.infile_original.copy()
        # If missing, add standardized columns to the list of in-file's columns
        for standard_column_name in self.table.col_names:
            if standard_column_name not in self.infile_original:
                standardized_infile_headers.append(standard_column_name)
        return standardized_infile_headers

    def set_infile_column_dtypes(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        dtypes = {}
        for col_name in self.infile_standardized:
            if not self.table.dtypes.get(col_name):
                dtypes.update({col_name: "TEXT"})
            else:
                dtypes.update({col_name: self.table.dtypes[col_name]})
        return dtypes


def insert_infile(
    infile: str | None,
    standardized_columns: list,
    connection: Connection,
    table_name: str,
    url_col: str | None = None,
):
    """_summary_

    Args:
        infile (str | None): _description_
        standardized_columns (list): _description_
        connection (Connection): _description_
        table_name (str): _description_
        url_col (str | None, optional): _description_. Defaults to None.
    """
    if not infile:
        pass
    else:
        executor = SQLiteWrapper(connection=connection)
        with open(infile) as f:
            reader = csv.DictReader(f)
            for row in reader:
                values = parse_rows(
                    row=row,
                    infile_standardized=standardized_columns,
                    url_col=url_col,
                )
                n_values = ", ".join(["?" for _ in range(len(values))])
                query = f"""
                INSERT OR IGNORE INTO {table_name} ({", ".join(standardized_columns)})
                VALUES ({n_values})
                """
                executor(query=query, values=values)  # type: ignore


def parse_rows(
    infile_standardized: List, row: Dict, url_col: str | None = None
) -> tuple:
    """_summary_

    Args:
        infile_standardized (List): _description_
        row (Dict): _description_
        url_col (str | None, optional): _description_. Defaults to None.

    Returns:
        tuple: _description_
    """
    values = []
    for col in infile_standardized:
        if col == "url" and url_col:
            values.append(row[url_col])
        elif row.get(col):
            values.append(row[col])
        else:
            values.append(None)
    return tuple(values)


def create_table(
    connection: Connection,
    dtype_string: str,
    table: LinksConstants | ShareContentConstants,
):
    executor = SQLiteWrapper(connection)
    table_name = table.table_name
    primary_key = table.primary_key

    query = f"DROP TABLE IF EXISTS {table_name}"
    executor(query=query)

    query = f"CREATE TABLE '{table_name}' ({dtype_string}, PRIMARY KEY ({primary_key}))"
    executor(query=query)
