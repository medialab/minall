# minall/tables/links.py

import csv
from dataclasses import dataclass
from pathlib import Path
from sqlite3 import Connection
from typing import Dict

import casanova

from minall.tables.base import BaseTable
from minall.tables.exceptions import NoCSVHeaders, NoURLColumn


@dataclass
class LinksConstants:
    """Dataclass to manage 'links' table.

    This dataclass manages the 'links' table's required column names and their data types.

    Attributes:
        table_name (str): Name of the table. Default = "links".
        primary_key (str): Text string of primary key. Default = "url".
        pk_list (list): List of primary key columns. Default = ["url"]
        dtypes (dict): Key-value pairs of column names and SQLite data type descriptions.
        col_names (list): List of column names.
    """

    table_name: str = "links"
    primary_key: str = "url"
    pk_list = ["url"]
    dtypes = {
        "url": "TEXT",
        "domain": "TEXT",
        "work_type": "TEXT",
        "duration": "TEXT",
        "identifier": "TEXT",
        "date_published": "TEXT",
        "date_modified": "TEXT",
        "country_of_origin": "TEXT",
        "abstract": "TEXT",
        "keywords": "TEXT",
        "title": "TEXT",
        "text": "TEXT",
        "hashtags": "TEXT",
        "creator_type": "TEXT",
        "creator_date_created": "TEXT",
        "creator_location_created": "TEXT",
        "creator_identifier": "TEXT",
        "creator_facebook_follow": "INTEGER",
        "creator_facebook_subscribe": "INTEGER",
        "creator_twitter_follow": "INTEGER",
        "creator_youtube_subscribe": "INTEGER",
        "creator_create_video": "INTEGER",
        "creator_name": "TEXT",
        "creator_url": "TEXT",
        "facebook_comment": "INTEGER",
        "facebook_like": "INTEGER",
        "facebook_share": "INTEGER",
        "pinterest_share": "INTEGER",
        "twitter_share": "INTEGER",
        "tiktok_share": "INTEGER",
        "tiktok_comment": "INTEGER",
        "reddit_engagement": "INTEGER",
        "youtube_watch": "INTEGER",
        "youtube_comment": "INTEGER",
        "youtube_like": "INTEGER",
        "youtube_favorite": "INTEGER",
        "youtube_subscribe": "INTEGER",
        "create_video": "INTEGER",
    }
    col_names = dtypes.keys()


class LinksTable(BaseTable):
    """Class for creating, updating, and reading SQL table for target URLs."""

    dtypes = LinksConstants.dtypes
    name = LinksConstants.table_name
    pk_list = LinksConstants.pk_list

    def __init__(
        self, conn: Connection, infile: Path, outfile: Path, url_col: str | None = None
    ):
        """In database connection, create SQL table and populate with data from target URLs dataset file.

        Args:
            conn (Connection): SQLite connection.
            infile (Path): Path to URLs dataset file.
            url_col (str | None, optional): Column name of target URLs. Defaults to None.

        Raises:
            NoCSVHeaders: Dataset file does not have headers.
            KeyError: User did not define URL column and dataset file does not have default column 'url'.
            NoURLColumn: User-defined URL column not found in dataset file.
        """
        # Update the table's columns to include all in-file columns
        self.dtypes = self._parse_infile_columns(
            infile=infile, url_col=url_col, constant_cols=self.dtypes
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
                if url_col:
                    row.update({"url": row[url_col]})
                placeholder = ", ".join(["?" for _ in range(len(row.items()))])
                cols, values = ", ".join(row.keys()), tuple(list(row.values()))
                query = """
                INSERT OR IGNORE INTO {table}({cols})
                VALUES ({placeholder})
                """.format(
                    table=self.name, cols=cols, placeholder=placeholder
                )
                self.execute(query=query, values=values)

    def _parse_infile_columns(
        self, infile: Path, constant_cols: Dict, url_col: str | None
    ) -> Dict:
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
        elif not url_col and not "url" in headers:
            raise KeyError()
        elif url_col and not url_col in headers:
            raise NoURLColumn(url_col=url_col)
        dtypes = {col: "TEXT" for col in headers}
        return dtypes | constant_cols
