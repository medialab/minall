from pathlib import Path

from minall.enrichment.enrichment import Enrichment
from minall.tables.base import BaseTable
from minall.tables.links.constants import LinksConstants
from minall.tables.shared_content.constants import ShareContentConstants
from minall.utils.database import connect_to_database
from minall.utils.parse_config import APIKeys


class Minall:
    def __init__(
        self,
        database: str | None,
        config: str | dict | None,
        output_dir: str,
        links_file: str,
        url_col: str,
        shared_content_file: str | None,
        buzzsumo_only: bool = False,
    ) -> None:
        # Connect to the SQLite database
        self.connection = connect_to_database(database=database)

        # Parse API keys from config file / dict
        self.keys = APIKeys(config=config)

        # Store Buzzsumo-only flag
        self.buzzsumo_only = buzzsumo_only

        # Set paths to output directory and out-files
        [p.mkdir(exist_ok=True) for p in Path(output_dir).parents]
        self.output_dir = Path(output_dir)
        self.links_file = self.output_dir.joinpath("links.csv")
        self.shared_contents_file = self.output_dir.joinpath("shared_content.csv")

        # Input original data into the database
        self.links_table = BaseTable(
            sqlite_connection=self.connection,
            infile=links_file,
            outfile=self.links_file,
            table=LinksConstants(),
            url_col=url_col,
        )

        self.shared_content_table = BaseTable(
            sqlite_connection=self.connection,
            infile=shared_content_file,
            outfile=self.shared_contents_file,
            table=ShareContentConstants(),
        )

    def collect_and_coalesce(self):
        """Collect new data and coalesce with existing data in SQL table."""
        enricher = Enrichment(
            links_table=self.links_table,
            shared_content_table=self.shared_content_table,
            keys=self.keys,
        )
        enricher(buzzsumo_only=self.buzzsumo_only)

    def export(self):
        self.links_table.export()
        self.shared_content_table.export()
