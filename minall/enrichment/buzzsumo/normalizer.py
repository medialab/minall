from datetime import datetime

import ural
from casanova import namedrecord
from ural.youtube import YOUTUBE_DOMAINS  # type: ignore


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

    def parse_buzzsumo_type(self, data: dict):
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
            if data.get(t) == 1:
                return "VideoObject"
        for t in article_types:
            if data.get(t) == 1:
                return "Article"

    def parse_timestamp(self, timestamp: str | None) -> datetime | None:
        if timestamp:
            try:
                ts = int(timestamp)
            except ValueError:
                return
            else:
                return datetime.fromtimestamp(ts)

    def __call__(self, url: str, link_id: str, data: dict) -> dict:
        domain = get_domain(url)

        buzzsumo_type = self.parse_buzzsumo_type(data=data)

        all_fields = {
            "url": url,
            "link_id": link_id,
            "domain": domain,
            "type": buzzsumo_type,
            "twitter_share": data.get("twitter_shares"),
            "facebook_share": data.get("total_facebook_shares"),
            "title": data.get("title"),
            "date_published": self.parse_timestamp(data.get("published_date")),
            "pinterest_share": data.get("pinterest_shares"),
            "creator_name": data.get("author_name"),
            "creator_identifier": data.get("twitter_user_id"),
            "duration": data.get("video_length"),
            "facebook_comment": data.get("facebook_comments"),
            "youtube_watch": data.get("youtube_views"),
            "youtube_like": data.get("youtube_likes"),
            "youtube_comment": data.get("youtube_comments"),
            "tiktok_share": data.get("tiktok_share_count"),
            "tiktok_comment": data.get("tiktok_comment_count"),
            "reddit_engagement": data.get("total_reddit_engagements"),
        }

        keep = {k: v for k, v in all_fields.items() if k in self.fields}

        return self.record(**keep).as_csv_dict_row()
