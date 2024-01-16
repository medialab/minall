# minall/tables/base.py

"""Create and execute queries on SQLite tables.

This module contains the class `BaseTable` that manages the SQLite database's tables. It contains the following methods:
"""

import csv
from pathlib import Path
from sqlite3 import Connection
from typing import Dict, Iterable, List, Tuple


class BaseTable:
    """Base class for SQLite tables."""

    def __init__(
        self, name: str, pk: List[str], conn: Connection, dtypes: Dict, outfile: Path
    ) -> None:
        """Create the SQL table with the given columns and data types.

        Args:
            name (str): Table name.
            pk (List[str]): List of primary keys.
            conn (Connection): SQLite connection.
            dtypes (Dict): Key-value pairs of column names and data types.
            outfile (Path): Path to CSV file where the table will be exported.
        """
        self.conn = conn
        self.name = name
        self.pk_list = pk
        self.pk_str = ",".join(pk)
        self.dtype_dict = dtypes
        self.outfile = outfile

        # Create the table
        self.execute(query=f"DROP TABLE IF EXISTS {self.name}")
        self.execute(query=self.create_query)

    def export(self, outfile: Path | None = None):
        """Write the SQL table to a CSV file.

        Args:
            outfile (Path | None, optional): Path to out-file. Defaults to None.
        """
        if not outfile:
            outfile = self.outfile
        cursor = self.conn.cursor()
        headers = [
            t[1]
            for t in cursor.execute(
                "SELECT * FROM pragma_table_info('{}');".format(self.name)
            ).fetchall()
        ]
        rows = cursor.execute(f"SELECT * FROM {self.name}").fetchall()
        with open(outfile, "w") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)

    def update_from_csv(self, datafile: Path):
        """Reading from a CSV file, update the table rows.

        Args:
            datafile (Path): Path to file with new data.
        """
        with open(datafile) as f:
            reader = csv.DictReader(f)
            for row in reader:
                placeholder = ", ".join(["?" for _ in range(len(row.items()))])
                cols_in_csv = ", ".join(row.keys())
                # Replace empty strings in values set with None
                values = []
                for v in row.values():
                    if v == "":
                        values.append(None)
                    else:
                        values.append(v)
                coalesce_stmt = self.coalesce_statement(row.keys())
                query = """
                INSERT INTO {table}({cols_in_csv})
                VALUES ({placeholder})
                ON CONFLICT ({pk})
                DO UPDATE SET {coalesce_stmt}
                """.format(
                    table=self.name,
                    cols_in_csv=cols_in_csv,
                    placeholder=placeholder,
                    pk=self.pk_str,
                    coalesce_stmt=coalesce_stmt,
                )
                self.execute(query=query, values=tuple(values))

    def coalesce_statement(self, cols: Iterable[str]) -> str:
        """Compose SQL coalesce statement from columns to be updated.

        Examples:
            >>> # Set up connection and columns / data types for table.
            >>> from minall.utils.database import connect_to_database
            >>> columns_n_datatypes = {"url": "TEXT", "domain": "TEXT", "work_type": "TEXT"}
            >>>
            >>> # Create table.
            >>> table = BaseTable(name="test", pk=["url"], conn=connect_to_database(), dtypes=columns_n_datatypes, outfile=Path("test.csv"))
            >>>
            >>> # Compose SQL statement to replace table's row with new data.
            >>> table.coalesce_statement(cols=columns_n_datatypes.keys())
            'domain=COALESCE(excluded.domain, domain), work_type=COALESCE(excluded.work_type, work_type)'

        Args:
            cols (Iterable[str]): Row columns.

        Returns:
            str: SQL statement.
        """
        return ", ".join(
            [f"{k}=COALESCE(excluded.{k}, {k})" for k in cols if k not in self.pk_list]
        )

    @property
    def create_query(self) -> str:
        """SQL statement to create table.

        Examples:
            >>> # Set up connection and columns / data types for table.
            >>> from minall.utils.database import connect_to_database
            >>> columns_n_datatypes = {"url": "TEXT", "domain": "TEXT", "work_type": "TEXT"}
            >>>
            >>> # Create table.
            >>> table = BaseTable(name="test", pk=["url"], conn=connect_to_database(), dtypes=columns_n_datatypes, outfile=Path("test.csv"))
            >>>
            >>> # Compose SQL statement to create table.
            >>> table.create_query
            >>> 'CREATE TABLE IF NOT EXISTS test(url TEXT, domain TEXT, work_type TEXT, PRIMARY KEY (url))'


        Returns:
            str: _description_
        """
        cols = ", ".join([f"{k} {v}" for k, v in self.dtype_dict.items()])
        return (
            """CREATE TABLE IF NOT EXISTS {table}({cols}, PRIMARY KEY ({pk}))""".format(
                table=self.name, cols=cols, pk=self.pk_str
            )
        )

    def execute(self, query: str, values: Tuple | None = None):
        """Function to commit a query to the database connection.

        Args:
            query (str): SQL statement.
            values (Tuple | None, optional): Values to be inserted in the query's placeholders. Defaults to None.

        Raises:
            e: SQLite Exception.
        """
        cursor = self.conn.cursor()
        try:
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
        except Exception as e:
            print("\n\n", query, "\n\n")
            raise e

    def select_from(self, cols: str, filter: str | None = None) -> List:
        """Function to select rows from the SQL table.

        Args:
            cols (str): Target of SELECT statement.
            filter (str | None, optional): Where condition to apply after FROM statement. Defaults to None.

        Raises:
            e: SQLite Exception.

        Returns:
            List: List of rows.
        """
        if not filter:
            filter = ""
        else:
            filter = " " + filter
        query = f"select {cols} from {self.name}{filter}"
        cursor = self.conn.cursor()
        try:
            response = cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print("\n\n", query, "\n\n")
            raise e
        else:
            return response.fetchall()
