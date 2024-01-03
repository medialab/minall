# minall/tables/cli.py

"""Create and execute queries on SQLite tables.

This module contains the class `BaseTable` that manages the SQLite database's tables. It contains the following methods:

- `__init__(sqlite_connection, infile, outfile, table, url_col)`
- `columns_to_update()`
- `coalesce(infile)`
- `export()`
"""

import csv
from pathlib import Path
from sqlite3 import Connection

from minall.tables.links.constants import LinksConstants
from minall.tables.shared_content.constants import ShareContentConstants
from minall.tables.utils import (
    ColumnParser,
    SQLiteWrapper,
    create_table,
    insert_infile,
    parse_rows,
)


class BaseTable:
    def __init__(
        self,
        sqlite_connection: Connection,
        infile: str | None,
        outfile: Path,
        table: LinksConstants | ShareContentConstants,
        url_col: str | None = None,
    ) -> None:
        """_summary_

        Args:
            sqlite_connection (Connection): _description_
            infile (str | None): _description_
            outfile (Path): _description_
            table (LinksConstants | ShareContentConstants): _description_
            url_col (str | None, optional): _description_. Defaults to None.
        """
        self.connection = sqlite_connection
        self.executor = SQLiteWrapper(sqlite_connection)
        self.outfile = outfile
        self.table = table
        self.columnparser = ColumnParser(
            connection=self.connection,
            table_constants=table,
            infile=infile,
            url_col=url_col,
        )

        # Create table upon creation of class instance
        create_table(
            connection=self.connection,
            dtype_string=self.columnparser.infile_dtype_string,
            table=self.table,
        )

        # Insert in-file data
        insert_infile(
            infile=infile,
            standardized_columns=self.columnparser.infile_standardized,
            connection=self.connection,
            url_col=url_col,
            table_name=self.table.table_name,
        )

    def columns_to_update(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        columns = []
        for column in self.columnparser.infile_standardized:
            if column not in self.table.pk_list:
                columns.append(f"{column}=COALESCE(excluded.{column}, {column})")
        return ", ".join(columns)

    def coalesce(self, infile: Path):
        """_summary_

        Args:
            infile (Path): _description_
        """
        table_columns = self.columnparser.infile_standardized
        columns_to_update = self.columns_to_update()
        with open(infile, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                values = parse_rows(infile_standardized=table_columns, row=row)
                n_values = ", ".join(["?" for _ in range(len(values))])
                query = f"""
                INSERT INTO {self.table.table_name} ({", ".join(table_columns)})
                VALUES ({n_values})
                ON CONFLICT ({self.table.primary_key})
                DO UPDATE SET {columns_to_update}
                """
                self.executor(query=query, values=values)  # type: ignore

    def export(self):
        """_summary_"""
        cursor = self.connection.cursor()
        rows = cursor.execute(f"SELECT * FROM {self.table.table_name}").fetchall()
        headers = self.columnparser.infile_standardized
        with open(self.outfile, "w") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)
