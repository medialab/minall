from pathlib import Path

import casanova
import duckdb
from duckdb import DuckDBPyConnection

from minall.links.constants import LINKS_DTYPES, LINKS_FIELDNAMES


class LinksTable:
    table_name = "links"

    def __init__(self, connection: DuckDBPyConnection) -> None:
        self.connection = connection

        # Create table if not exists
        columns = ", ".join([k + " " + v for k, v in LINKS_DTYPES.items()])
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} ({columns}, PRIMARY KEY (url, link_id))
        """
        self.connection.sql(sql)

    def insert(self, infile: Path):
        # Read the CSV file into a view (virtual table, not written to database)
        infile_fieldnames = casanova.reader(infile).fieldnames
        if not infile_fieldnames:
            raise KeyError
        print(f"\n\tInserting file '{infile}' to table '{self.table_name}'")
        file_name = str(infile)
        self.connection.sql("DROP VIEW IF EXISTS links_view")
        sql = f"""
        CREATE VIEW 'links_view' ({", ".join(infile_fieldnames)})
        AS SELECT {", ".join(infile_fieldnames)} FROM read_csv_auto('{file_name}', header=True)
        """
        self.connection.sql(sql)

        # Insert new values into the appearances table
        if sorted(infile_fieldnames) == sorted(["url", "link_id"]):
            sql = f"""
            INSERT INTO {self.table_name} ({", ".join(infile_fieldnames)})
            SELECT * FROM 'links_view'
            ON CONFLICT (url, link_id)
            DO NOTHING
            """
        else:
            fields_without_primary_key = LINKS_FIELDNAMES.copy()
            fields_without_primary_key.remove("url")
            fields_without_primary_key.remove("link_id")
            updated_fields = [
                f"{field} = COALESCE(excluded.{field}, {self.table_name}.{field})"
                for field in fields_without_primary_key
            ]
            sql = f"""
            INSERT INTO {self.table_name} ({", ".join(infile_fieldnames)})
            SELECT * FROM 'links_view'
            ON CONFLICT (url, link_id)
            DO UPDATE SET {", ".join(updated_fields)}
            """
        self.connection.sql(sql)

    def export(self, outfile: Path):
        print(f"\n\tWriting table '{self.table_name}' to path '{outfile}'")
        file_name = str(outfile)
        duckdb.table(self.table_name, connection=self.connection).write_csv(
            file_name=file_name, header=True
        )  # type: ignore
