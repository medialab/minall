import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from duckdb import DuckDBPyConnection

from minall.links.links_table import LinksTable
from minall.shared_content.shared_content_table import SharedContentTable

bar = "\n===============\n"


def setup_database(connection: DuckDBPyConnection):
    links_table = LinksTable(connection=connection)
    shared_content_table = SharedContentTable(connection=connection)

    # Get user-defined file paths
    load_dotenv(find_dotenv())
    input_links_file = os.getenv("INPUT_LINKS")
    input_shared_content = os.getenv("INPUT_SHARED_CONTENT")
    output_dir = os.getenv("OUTPUT_DIR")
    if not input_links_file or not output_dir:
        raise KeyError
    outdir = Path(output_dir)
    links_outfile = outdir.joinpath("links.csv")
    shared_content_outfile = outdir.joinpath("shared_content.csv")

    print(f"{bar}Initializing in-memory database")

    # If available, import data from shared content
    if input_shared_content is not None:
        shared_content_table.insert(infile=Path(input_shared_content))

    # Import data from input file of links
    links_table.insert(infile=Path(input_links_file))

    # Export tables to working data directory
    shared_content_table.export(outfile=shared_content_outfile)
    links_table.export(outfile=links_outfile)
