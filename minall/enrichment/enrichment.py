# minall/enrichment/enrichment.py

"""Class for data collection and coalescing.

With the class `Enrichment`, this module manages the data collection process.

The class contains the following methods:

- `__init__(links_table, shared_content_table, keys)` - 
"""

from minall.enrichment.article_text import get_article_text
from minall.enrichment.buzzsumo import get_buzzsumo_data
from minall.enrichment.crowdtangle import get_facebook_post_data
from minall.enrichment.other_social_media import add_type_data
from minall.enrichment.utils import FilteredLinks, apply_domain
from minall.enrichment.youtube import get_youtube_data
from minall.tables.links import LinksTable
from minall.tables.shared_content import SharedContentTable
from minall.utils.database import SQLiteWrapper
from minall.utils.parse_config import APIKeys

bar = "\n===============\n"


class Enrichment:
    def __init__(
        self,
        links_table: LinksTable,
        shared_content_table: SharedContentTable,
        keys: APIKeys,
    ) -> None:
        """From given API keys and URL data set, filter URLs by domain and initialize data enrichment class.

        Args:
            links_table (BaseTable): BaseTable class instance of SQL table for URL dataset.
            shared_content_table (BaseTable): BaseTable class instance of SQL table for shared content related to URLs in dataset.
            keys (APIKeys): APIKeys class instance of minet API client configurations.
        """

        self.links_table = links_table
        self.shared_content_table = shared_content_table
        self.keys = keys
        self.filtered_links = FilteredLinks(self.links_table)

    def buzzsumo(self):
        """For all URLs, collect data from Buzzsumo and coalesce in the database's 'links' table."""

        if self.keys.buzzsumo_token:
            get_buzzsumo_data(
                data=self.filtered_links.all_links,
                token=self.keys.buzzsumo_token,
                outfile=self.links_table.outfile,
            )
            self.links_table.update_from_csv(datafile=self.links_table.outfile)

    def scraper(self):
        """For select URLs, collect data via scraping and coalesce in the database's 'links' table."""

        # In multiple threads, scrape HTML data and write to a CSV file
        get_article_text(
            data=self.filtered_links.to_scrape, outfile=self.links_table.outfile
        )
        # Coalesce the results in the CSV File to the links table
        self.links_table.update_from_csv(datafile=self.links_table.outfile)

    def other_social_media(self):
        """For select URLs, update the 'work_type' column in the database's 'links' table with the value 'SocialMediaPosting'."""
        # Assign default type to social media post
        add_type_data(
            data=self.filtered_links.other_social, outfile=self.links_table.outfile
        )
        # Coalesce the results in the CSV File to the links table
        self.links_table.update_from_csv(datafile=self.links_table.outfile)

    def facebook(self):
        """For Facebook URLs, collect data from CrowdTangle and coalesce in the database's 'links' and 'shared_content' tables."""
        if self.keys.crowdtangle_token:
            get_facebook_post_data(
                data=self.filtered_links.facebook,
                token=self.keys.crowdtangle_token,
                rate_limit=self.keys.crowdtangle_rate_limit,
                links_outfile=self.links_table.outfile,
                shared_content_outfile=self.shared_content_table.outfile,
            )
            # Coalesce the results in the CSV File to the links table
            self.links_table.update_from_csv(datafile=self.links_table.outfile)
            self.shared_content_table.update_from_csv(
                datafile=self.shared_content_table.outfile
            )

    def youtube(self):
        """For YouTube URLs, collect data from YouTube API and coalesce in the database's 'links' table."""
        if self.keys.youtube_key:
            # In single thread, collect YouTube API data and write to a CSV file
            get_youtube_data(
                data=self.filtered_links.youtube,
                keys=self.keys.youtube_key,
                outfile=self.links_table.outfile,
            )
            # Coalesce the results in the CSV File to the links table
            self.links_table.update_from_csv(datafile=self.links_table.outfile)

    def __call__(self, buzzsumo_only: bool):
        executor = SQLiteWrapper(connection=self.links_table.conn)
        # apply domain to all urls
        for link in self.filtered_links.all_links:
            query, domain = apply_domain(link)
            if query and domain:
                self.links_table.conn
                executor(query=query)

        if not buzzsumo_only:
            if len(self.filtered_links.youtube) > 0:
                self.youtube()
            if len(self.filtered_links.facebook) > 0:
                self.facebook()
            if len(self.filtered_links.other_social) > 0:
                self.other_social_media()
            if len(self.filtered_links.to_scrape) > 0:
                self.scraper()
        self.buzzsumo()
