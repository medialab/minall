from pathlib import Path

import duckdb
from duckdb import DuckDBPyConnection

from minall.shared_content.constants import (
    SHARED_CONTENT_DTYPES,
    SHARED_CONTENT_FIELDNAMES,
)


class SharedContentTable:
    table_name = "shared_content"

    def __init__(self, connection: DuckDBPyConnection) -> None:
        self.connection = connection

        # Create table if not exists
        columns = ", ".join([k + " " + v for k, v in SHARED_CONTENT_DTYPES.items()])
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} ({columns}, PRIMARY KEY (post_url, content_url))
        """
        self.connection.sql(sql)

    def insert(self, infile: Path):
        # Read the CSV file into a view (virtual table, not written to database)
        print(f"\n\tInserting file '{infile}' to table '{self.table_name}'")
        file_name = str(infile)
        self.connection.sql("DROP VIEW IF EXISTS shared_content_view")
        sql = f"""
        CREATE VIEW 'shared_content_view' ({", ".join(SHARED_CONTENT_FIELDNAMES)})
        AS SELECT * FROM read_csv_auto('{file_name}', header=True)
        """
        self.connection.sql(sql)

        # Insert new values into the appearances table
        fields_without_primary_key = SHARED_CONTENT_FIELDNAMES.copy()
        fields_without_primary_key.remove("post_url")
        fields_without_primary_key.remove("content_url")
        updated_fields = [
            f"{field} = COALESCE(excluded.{field}, {self.table_name}.{field})"
            for field in fields_without_primary_key
        ]
        sql = f"""
        INSERT INTO {self.table_name} ({", ".join(SHARED_CONTENT_FIELDNAMES)})
        SELECT * FROM 'shared_content_view'
        ON CONFLICT (post_url, content_url)
        DO UPDATE SET {", ".join(updated_fields)}
        """
        self.connection.sql(sql)

    def export(self, outfile: Path):
        print(f"\n\tWriting table '{self.table_name}' to path '{outfile}'")
        file_name = str(outfile)
        duckdb.table(self.table_name, connection=self.connection).write_csv(
            file_name=file_name, header=True
        )  # type: ignore
