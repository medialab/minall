from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from casanova import TabularRecord
from minet.buzzsumo.types import BuzzsumoArticle

from minall.enrichment.utils import get_domain

BEGINDATE = int(datetime.strptime("2020-01-01", "%Y-%m-%d").timestamp())

ENDDATE = int(
    datetime.strptime(
        datetime.utcnow().isoformat().split("T")[0], "%Y-%m-%d"
    ).timestamp()
)


@dataclass
class NormalizedBuzzsumoResult(TabularRecord):
    url: str
    work_type: str
    domain: Optional[str]
    twitter_share: Optional[int]
    facebook_share: Optional[int]
    title: Optional[str]
    date_published: Optional[datetime]
    pinterest_share: Optional[int]
    creator_name: Optional[str]
    creator_identifier: Optional[str]
    duration: Optional[int]
    facebook_comment: Optional[int]
    youtube_watch: Optional[int]
    youtube_like: Optional[int]
    youtube_comment: Optional[int]
    tiktok_share: Optional[int]
    tiktok_comment: Optional[int]
    reddit_engagement: Optional[int]

    @classmethod
    def parse_buzzsumo_type(cls, data: BuzzsumoArticle | None) -> str:
        video_types = ["is_video"]
        article_types = [
            "is_general_article",
            "is_how_to_article",
            "is_infographic",
            "is_interview",
            "is_list",
            "is_newsletter",
            "is_press_release",
            "is_review",
            "is_what_post",
            "is_why_post",
        ]
        work_type = "MediaObject"
        if data:
            for t in video_types:
                if getattr(data, t):
                    return "VideoObject"
            for t in article_types:
                if getattr(data, t):
                    return "Article"
        return work_type

    @classmethod
    def from_payload(
        cls,
        url: str,
        data: BuzzsumoArticle | None,
    ) -> "NormalizedBuzzsumoResult":
        return NormalizedBuzzsumoResult(
            url=url,
            domain=get_domain(url),
            work_type=cls.parse_buzzsumo_type(data),
            twitter_share=getattr(data, "twitter_shares"),
            facebook_share=getattr(data, "facebook_shares"),
            title=getattr(data, "title"),
            date_published=getattr(data, "published_date"),
            pinterest_share=getattr(data, "pinterest_shares"),
            creator_name=getattr(data, "author_name"),
            creator_identifier=getattr(data, "twitter_user_id"),
            duration=getattr(data, "video_length"),
            facebook_comment=getattr(data, "facebook_comments"),
            youtube_watch=getattr(data, "youtube_views"),
            youtube_like=getattr(data, "youtube_likes"),
            youtube_comment=getattr(data, "youtube_comments"),
            tiktok_share=getattr(data, "tiktok_share_count"),
            tiktok_comment=getattr(data, "tiktok_comment_count"),
            reddit_engagement=getattr(data, "total_reddit_engagements"),
        )
