import click
import duckdb

from minall.enrichment.enrichment import enrich_links
from minall.export_db import export_database
from minall.setup_db import setup_database
from minall.utils import parse_cli_args


@click.command()
@click.option(
    "--input-links",
    "-i",
    "links",
    required=True,
    type=str,
    help="Path to file of URLs to be enriched",
)
@click.option(
    "--input-shared-content",
    "-s",
    "shared_content",
    required=False,
    type=str,
    help="Path to file of shared media content",
)
@click.option(
    "--output-dir",
    "-o",
    "output_dir",
    required=True,
    type=str,
    help="Path to directory for enriched files",
)
@click.option(
    "--buzzsumo-only",
    "-b",
    "buzzsumo_only",
    show_default=True,
    required=False,
    default=False,
    type=bool,
)
@click.option(
    "--config-file",
    "-c",
    "config_file",
    required=True,
    type=str,
    help="Path to file with API keys and configuration details",
)
def cli(links, shared_content, output_dir, buzzsumo_only, config_file):
    # Parse CLI options
    parse_cli_args(
        links_file=links,
        shared_content_file=shared_content,
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


if __name__ == "__main__":
    cli()
