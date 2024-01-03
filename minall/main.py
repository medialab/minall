# minall/main.py

"""Minall enrichment workflow.

With the class `Minall`, this module manages the entire workflow.

The class contains the following methods:

- `__init__(database, config, output_dir, links_file, url_col, shared_content_file, buzzsumo_only)` - Intialize SQLite database and out-file paths.
- `collect_and_coalesce()` - Collect new data and coalesce with existing data in relevant SQL tables.
- `export()` - Write enriched SQL tables to CSV out-files.
"""

from pathlib import Path
from typing import Tuple

from minall.enrichment.enrichment import Enrichment
from minall.tables.base import BaseTable
from minall.tables.links.constants import LinksConstants
from minall.tables.shared_content.constants import ShareContentConstants
from minall.utils.database import connect_to_database
from minall.utils.parse_config import APIKeys


class Minall:
    """Class to store variables and execute steps of enrichment."""

    def __init__(
        self,
        database: str | None,
        config: str | dict | None,
        output_dir: str,
        links_file: str,
        url_col: str,
        shared_content_file: str | None = None,
        buzzsumo_only: bool = False,
    ) -> None:
        """Intialize SQLite database and out-file paths.

        Args:
            database (str | None): Path name to SQLite database. If None, creates database in memory.
            config (str | dict | None): Credentials for API keys.
            output_dir (str): Path name to directory for enriched CSV files.
            links_file (str): Path name to in-file for URLs.
            url_col (str): Name of URL column in URLs file.
            shared_content_file (str | None): Path name to CSV file of shared content related to URLs.
            buzzsumo_only (bool, optional): Whether to only run Buzzsumo enrichment. Defaults to False.
        """

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
        """Collect new data and coalesce with existing data in relevant SQL tables."""
        enricher = Enrichment(
            links_table=self.links_table,
            shared_content_table=self.shared_content_table,
            keys=self.keys,
        )
        enricher(buzzsumo_only=self.buzzsumo_only)

    def export(self) -> Tuple[Path, Path]:
        """Write enriched SQL tables to CSV out-files.

        Returns:
            Tuple[Path, Path]: Paths to links and shared content CSV files.
        """
        self.links_table.export()
        self.shared_content_table.export()
        return self.links_file, self.shared_contents_file
