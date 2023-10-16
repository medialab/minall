import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from duckdb import DuckDBPyConnection

from minall.links.links_table import LinksTable
from minall.shared_content.shared_content_table import SharedContentTable


def export_database(connection: DuckDBPyConnection):
    links_table = LinksTable(connection=connection)
    shared_content_table = SharedContentTable(connection=connection)

    # Get user-defined file paths
    load_dotenv(find_dotenv())
    output_dir = os.getenv("OUTPUT_DIR")
    if not output_dir:
        raise KeyError
    outdir = Path(output_dir)
    links_outfile = outdir.joinpath("links.csv")
    shared_content_outfile = outdir.joinpath("shared_content.csv")

    links_table.export(outfile=links_outfile)
    shared_content_table.export(outfile=shared_content_outfile)
