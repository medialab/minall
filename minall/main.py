# minall/main.py

"""Minall enrichment workflow.

With the class `Minall`, this module manages the entire workflow.

The class contains the following methods:

- `__init__(database, config, output_dir, links_file, url_col, shared_content_file, buzzsumo_only)` - Intialize SQLite database and out-file paths.
- `collect_and_coalesce()` - Collect new data and coalesce with existing data in relevant SQL tables.
- `export()` - Write enriched SQL tables to CSV out-files.
"""

import os
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

        Examples:
            >>> # Set file path variables.
            >>> OUT_DIR = Path(__file__).parent.parent.joinpath("docs").joinpath("doctest")
            >>> LINKS_FILE = OUT_DIR.joinpath('minall_init_example.csv')
            >>>
            >>> # Create Minall instance.
            >>> minall = Minall(database=None, config={}, output_dir=str(OUT_DIR), links_file=str(LINKS_FILE), url_col='target_url')
            >>> minall.links_table.table
            LinksConstants(table_name='links', primary_key='url')
            >>>
            >>> # Check that Minall's SQLite database connection has committed 1 change (creating the 'links' table).
            >>> minall.connection.total_changes
            1

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
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        [p.mkdir(exist_ok=True) for p in self.output_dir.parents]
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
        """Collect new data and coalesce with existing data in relevant SQL tables.

        This method creates an instance of the class `Enrichment` (from `minall.enrichment.enrichment`), providing the target URL table ('links' table, `self.links_table`), the minet API credentials (`self.keys`), and the related shared content table (`self.shared_content_table`) which may go unused depending on parameters used when `Enrichment` is called.

        Having prepared the `Enrichment` instance, the method then calls the class, providing its `self.buzzsumo_only` instance attribute as the argument for `Enrichment`'s `buzzsumo_only` parameter. The latter boolean parameter determines whether all of the `Enrichment` class's methods will be deployed or only its Buzzsumo method.
        """
        enricher = Enrichment(
            links_table=self.links_table,
            shared_content_table=self.shared_content_table,
            keys=self.keys,
        )
        enricher(buzzsumo_only=self.buzzsumo_only)

    def export(self) -> Tuple[Path, Path]:
        """Write enriched SQL tables to CSV out-files.

        This method simply exports to CSV files both of the `Minall` class instance's SQL tables, `self.links_table` and `self.shared_content_table`. The class that manages the SQL tables (`minall.tables.base.BaseTable`), stores each table's out-file path as an instance variable. The parent directory for both out-files was declared during `Minall`'s `__init__()` method via the parameter `output_dir`, from which the out-file paths were subsequently derived.

        Returns:
            Tuple[Path, Path]: Paths to links and shared content CSV files.
        """
        self.links_table.export()
        self.shared_content_table.export()
        return self.links_file, self.shared_contents_file
