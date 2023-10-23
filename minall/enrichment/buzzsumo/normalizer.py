from datetime import datetime

import ural
from casanova import namedrecord
from ural.youtube import YOUTUBE_DOMAINS  # type: ignore

from minall.enrichment.buzzsumo.constants import BuzzsumoResult


def get_domain(url: str):
    domain_name = ural.get_domain_name(url)
    if domain_name in YOUTUBE_DOMAINS:
        domain_name = "youtube.com"
    return domain_name


class BuzzsumoNormalizer:
    def __init__(self, fields: list) -> None:
        self.record = namedrecord(
            "Record", fields=fields, defaults=[None for _ in range(len(fields))]
        )
        self.fields = fields

    def parse_buzzsumo_type(self, data: BuzzsumoResult):
        video_types = ["video"]
        article_types = [
            "general_article",
            "how_to_article",
            "infographic",
            "interview",
            "list",
            "newsletter",
            "press_release",
            "review",
            "what_post",
            "why_post",
        ]
        for t in video_types:
            if getattr(data, t) == 1:
                return "VideoObject"
        for t in article_types:
            if getattr(data, t) == 1:
                return "Article"

    def parse_timestamp(self, timestamp: str | None) -> datetime | None:
        if timestamp:
            try:
                ts = int(timestamp)
            except ValueError:
                return
            else:
                return datetime.fromtimestamp(ts)

    def __call__(self, url: str, link_id: str, data: BuzzsumoResult) -> dict:
        domain = get_domain(url)

        buzzsumo_type = self.parse_buzzsumo_type(data=data)

        all_fields = {
            "url": url,
            "link_id": link_id,
            "domain": domain,
            "type": buzzsumo_type,
            "twitter_share": getattr(data, "twitter_shares"),
            "facebook_share": getattr(data, "total_facebook_shares"),
            "title": getattr(data, "title"),
            "date_published": self.parse_timestamp(getattr(data, "published_date")),
            "pinterest_share": getattr(data, "pinterest_shares"),
            "creator_name": getattr(data, "author_name"),
            "creator_identifier": getattr(data, "twitter_user_id"),
            "duration": getattr(data, "video_length"),
            "facebook_comment": getattr(data, "facebook_comments"),
            "youtube_watch": getattr(data, "youtube_views"),
            "youtube_like": getattr(data, "youtube_likes"),
            "youtube_comment": getattr(data, "youtube_comments"),
            "tiktok_share": getattr(data, "tiktok_share_count"),
            "tiktok_comment": getattr(data, "tiktok_comment_count"),
            "reddit_engagement": getattr(data, "total_reddit_engagements"),
        }

        keep = {k: v for k, v in all_fields.items() if k in self.fields}

        return self.record(**keep).as_csv_dict_row()
