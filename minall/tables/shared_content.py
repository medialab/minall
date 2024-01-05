# minall/tables/shared_content.py


import csv
from dataclasses import dataclass
from pathlib import Path
from sqlite3 import Connection
from typing import Dict

import casanova

from minall.tables.base import BaseTable
from minall.tables.exceptions import NoCSVHeaders, NoPrimaryKeyColumns
from minall.tables.links import LinksConstants


@dataclass
class ShareContentConstants:
    """Dataclass to manage 'shared_content' table.

    This dataclass manages the 'shared_content' table's required column names and their data types. Being a dataclass, however, the instance of the class can also be subsequently modified to include other column names (and their data types) according to the input data. The 'shared_content' table is meant to relate to the 'links' table, wherein the former's 'post_url' column refers to the latter's 'url' column.

    Contrary to the 'links' table, whose primary key column can be derived from any declared target URL column in the input data, the 'shared_content' table requires the input data has the two columns that jointly compose its primary key, 'post_url' and 'content_url.'

    Attributes:
        table_name (str): Name of the table. Default = "shared_content".
        primary_key (str): Text string of composite primary key. Default = "post_url,content_url".
        pk_list (list): List of comosite primary key columns. Default = ["post_url", "content_url]
        dtypes (dict): Key-value pairs of column names and SQLite data type descriptions.
        col_names (list): List of column names.
    """

    table_name = "shared_content"
    primary_key = "post_url,content_url"
    pk_list = ["post_url", "content_url"]
    dtypes = {
        "post_url": f"TEXT REFERENCES {LinksConstants.table_name}(url) ON UPDATE CASCADE",
        "media_type": "TEXT",
        "content_url": "TEXT",
        "height": "INTEGER",
        "width": "INTEGER",
    }
    col_names = dtypes.keys()


class SharedContentTable(BaseTable):
    """Class for creating, updating, and reading SQL table for shared media content, each of which is related to 1 or more entities in the 'links' table."""

    dtypes = ShareContentConstants.dtypes
    name = ShareContentConstants.table_name
    pk_list = ShareContentConstants.pk_list

    def __init__(self, conn: Connection, infile: Path | None, outfile: Path):
        """In database connection, create SQL table. If the user provides an existing shared_content.csv file, populate the table with that input.

        Args:
            conn (Connection): SQLite connection.
            infile (Path): Path to shared content dataset file.

        Raises:
            NoCSVHeaders: Dataset file does not have headers.
            NoPrimaryKeyColumns: One or more of the required columns ('post_url', 'content_url') is not in the dataset file.
        """
        # Update the table's columns to include all in-file columns
        if infile:
            self.dtypes = self._parse_infile_columns(
                infile=infile, constant_cols=self.dtypes
            )
        # Inherit the parent base class
        super().__init__(
            name=self.name,
            pk=self.pk_list,
            dtypes=self.dtypes,
            conn=conn,
            outfile=outfile,
        )

        # Insert in-file data
        if infile:
            with open(infile) as f:
                reader = csv.DictReader(f)

                # Confirm the in-file is compatible with the table
                headers = reader.fieldnames
                if not headers:
                    raise NoCSVHeaders()
                elif len(set(headers).difference(self.dtype_dict.keys())) > 0:
                    raise KeyError()

                # Insert the in-file data
                for row in reader:
                    placeholder = ", ".join(["?" for _ in range(len(row.items()))])
                    cols, values = ", ".join(row.keys()), tuple(list(row.values()))
                    query = """
                    INSERT OR IGNORE INTO {table}({cols})
                    VALUES ({placeholder})
                    """.format(
                        table=self.name, cols=cols, placeholder=placeholder
                    )
                    self.execute(query=query, values=values)

    def _parse_infile_columns(self, infile: Path, constant_cols: Dict) -> Dict:
        """During init method, modify table columns to include in-file's columns.

        Args:
            infile (Path): Path to URLs dataset.
            constant_cols (Dict): Key-value pairs of table's standard columns and data types.
            url_col (str | None, optional): Column name of target URLs.

        Raises:
            NoCSVHeaders: The infile does not have headers.
            KeyError: The infile does not have a recognizable URL column.
            NoURLColumn: The infile does not have the user-declared URL column.

        Returns:
            Dict: Key-value pairs of table's column names and data types.
        """
        with casanova.reader(infile) as reader:
            headers = reader.headers
        if not headers:
            raise NoCSVHeaders()
        diff = set(self.pk_list).difference(headers)
        if len(diff) > 0:
            raise NoPrimaryKeyColumns(col=list(diff)[0])
        dtypes = {col: "TEXT" for col in headers}
        return dtypes | constant_cols
