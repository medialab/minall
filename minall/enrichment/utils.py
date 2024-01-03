# minall/enrichment/utils.py

"""Functions for data collection.

This module provides the following class and functions:

- `get_domain(url)` - Parse domain from URL string.
- `apply_domain(url)` - Generate SQL query to insert domain into table.
- `FilteredLinks(table)` - From SQL table, select subsets of URLs based on domain name.
"""

from typing import List, Tuple

import ural
from ural.facebook import is_facebook_url
from ural.youtube import YOUTUBE_DOMAINS  # type: ignore
from ural.youtube import is_youtube_url

from minall.tables.base import BaseTable
from minall.tables.links.constants import LinksConstants


def get_domain(url: str) -> str | None:
    """Parse the domain name of a given URL string.

    Examples:
        >>> get_domain(url="https://www.youtube.com/channel/MkDocs")
        'youtube.com'

    Args:
        url (str): URL string.

    Returns:
        str | None: If successfully parsed, domain name.
    """

    domain_name = ural.get_domain_name(url)
    if domain_name in YOUTUBE_DOMAINS:
        domain_name = "youtube.com"
    return domain_name


def apply_domain(url: str) -> Tuple[str | None, str | None]:
    """Compose SQL query to update the domain column of a URL's row in the 'links' SQLite table.

    Examples:
        >>> apply_domain(url="https://www.youtube.com/channel/MkDocs")
        ("UPDATE links SET domain = 'youtube.com' WHERE url = 'https://www.youtube.com/channel/MkDocs'", 'youtube.com')

    Args:
        url (str): URL string.

    Returns:
        Tuple[str | None, str | None]: If domain was parsed, a tuple containing the SQL query and domain name.
    """

    query = None
    domain = get_domain(url)
    if domain:
        query = f"UPDATE {LinksConstants.table_name} SET domain = '{domain}' WHERE {LinksConstants.primary_key} = '{url}'"
    return query, domain


class FilteredLinks:
    """Selects all URLs from SQL table and returns subsets."""

    def __init__(self, table: BaseTable) -> None:
        """Select and store all URLs from a target SQL table.

        Args:
            table (BaseTable): Target SQL table.
        """
        cursor = table.connection.cursor()
        self.all_links = [
            row[0]
            for row in cursor.execute(
                f"SELECT url FROM {table.table.table_name}"
            ).fetchall()
        ]

    @property
    def youtube(self) -> List[str]:
        """List of URLs from YouTube.

        Returns:
            List[str]: List of URL strings.
        """
        return [url for url in self.all_links if is_youtube_url(url=url)]

    @property
    def facebook(self) -> List[str]:
        """List of URLs from Facebook.

        Returns:
            List[str]: List of URL strings.
        """
        return [url for url in self.all_links if is_facebook_url(url=url)]

    @property
    def other_social(self) -> List[str]:
        """List of URLs from social media platforms.

        Returns:
            List[str]: List of URL strings.
        """
        return [
            url
            for url in self.all_links
            if get_domain(url=url)
            in [
                "facebook.com",
                "youtube.com",
                "tiktok.com",
                "instagram.com",
                "twitter.com",
                "snapchat.com",
            ]
        ]

    @property
    def to_scrape(self) -> List[str]:
        """List of URLs not from social media platforms.

        Returns:
            List[str]: List of URL strings.
        """
        return [
            url
            for url in self.all_links
            if get_domain(url=url)
            not in [
                "facebook.com",
                "youtube.com",
                "tiktok.com",
                "instagram.com",
                "twitter.com",
                "snapchat.com",
            ]
        ]
