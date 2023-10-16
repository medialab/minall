import click
import duckdb

from minall.enrichment.enrichment import enrich_links
from minall.export_db import export_database
from minall.setup_db import setup_database
from minall.utils import parse_cli_args


def process_new_set(
    links_file: str,
    output_dir: str,
    config_file: str,
    shared_content_file: str | None = None,
    buzzsumo_only: bool = False,
):
    parse_cli_args(
        links_file=links_file,
        shared_content_file=shared_content_file,
        output_dir=output_dir,
        buzzsumo_only=buzzsumo_only,
        config_file=config_file,
    )

    # Connect to in-memory database and create tables with input data
    db_connection = duckdb.connect(":memory:")
    setup_database(connection=db_connection)

    # Enrich links
    enrich_links(connection=db_connection)

    # Export data
    export_database(connection=db_connection)
