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
        columns = []
        for column in self.columnparser.infile_standardized:
            if column not in self.table.pk_list:
                columns.append(f"{column}=COALESCE(excluded.{column}, {column})")
        return ", ".join(columns)

    def coalesce(self, infile: Path):
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
        cursor = self.connection.cursor()
        rows = cursor.execute(f"SELECT * FROM {self.table.table_name}").fetchall()
        headers = self.columnparser.infile_standardized
        with open(self.outfile, "w") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)
