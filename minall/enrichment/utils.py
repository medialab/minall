from sqlite3 import Connection

import ural
from ural.facebook import is_facebook_url
from ural.youtube import YOUTUBE_DOMAINS  # type: ignore
from ural.youtube import is_youtube_url

from minall.tables.base import BaseTable


def get_domain(url: str):
    domain_name = ural.get_domain_name(url)
    if domain_name in YOUTUBE_DOMAINS:
        domain_name = "youtube.com"
    return domain_name


class FilteredLinks:
    def __init__(self, table: BaseTable) -> None:
        cursor = table.connection.cursor()
        self.all_links = [
            row[0]
            for row in cursor.execute(
                f"SELECT url FROM {table.table.table_name}"
            ).fetchall()
        ]

    @property
    def youtube(self):
        return [url for url in self.all_links if is_youtube_url(url=url)]

    @property
    def facebook(self):
        return [url for url in self.all_links if is_facebook_url(url=url)]

    @property
    def other_social(self):
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
    def to_scrape(self):
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