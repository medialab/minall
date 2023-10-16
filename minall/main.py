import duckdb
import typer

from minall.enrichment.enrichment import enrich_links
from minall.export_db import export_database
from minall.setup_db import setup_database
from minall.utils import parse_cli_args


def main():
    # Parse CLI arguments
    parse_cli_args()

    # Connect to in-memory database and create tables with input data
    db_connection = duckdb.connect(":memory:")
    setup_database(connection=db_connection)

    # Enrich links
    enrich_links(connection=db_connection)

    # Export data
    export_database(connection=db_connection)


if __name__ == "__main__":
    typer.run(main)
