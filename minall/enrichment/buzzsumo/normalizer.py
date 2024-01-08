# minall/enrichment/buzzsumo/normalizer.py

"""Module contains constants for minet's Buzzsumo API client and a dataclass to normalize minet's Buzzsumo result.
"""

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
    """Dataclass to normalize minet's Buzzsumo API result.

    Attributes:
        url (str): Target URL searched in Buzzsumo database.
        work_type (str): Target URL's schema subtype, i.e. "WebPage", "Article", "VideoObject".
        twitter_share (int): Number of times the target URL appeared on Twitter.
        facebook_share (int): Number of times the target URL appeared on Facebook.
        title (str): Title of target URL web content.
        date_published (datetime): Date target URL web content was published.
        pinterest_share (int): Number of times the target URL appeared on Pinterest.
        creator_name (str): Entity intellectually responsible for (author of) the target URL's web content.
        creator_identifier (str): If target URL is a social media post, the platform's identifier for the author.
        duration (int): If the target URL is of a video, the video's duration.
        facebook_comment (int): Number of times Facebook users commented on a post containing the target URL.
        youtube_watch (int): If the target URL is of a YouTube video, number of times YouTube users watched the video.
        youtube_like (int): If the target URL is of a YouTube video, number of times YouTube users liked the video.
        tiktok_share (int): If the target URL is of TikTok content, number of shares on TikTok.
        tiktok_comment (int): If the target URL is of TikTok content, number of times TikTok users commented on the content.
        reddit_engagement (int): Number of times the target URL appeared on Reddit.
    """

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
        """Helper function for transforming Buzzsumo's content classification into Schema.org subtype.

        Args:
            data (BuzzsumoArticle | None): If target URL was found in Buzzsumo database, minet's result; otherwise, None.

        Returns:
            str: Schema for web content's subtype.
        """
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
        work_type = "WebPage"
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
        """Parses minet's Buzzsumo result and creates normalized dataclass.

        Args:
            url (str): Target URL searched in Buzzsumo's database.
            data (BuzzsumoArticle | None): If target URL was found in Buzzsumo database, minet's result; otherwise, None.

        Returns:
            NormalizedBuzzsumoResult: Dataclass that normalizes minet's Buzzsumo result object.
        """
        if data:
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
        else:
            return NormalizedBuzzsumoResult(
                url=url,
                work_type=cls.parse_buzzsumo_type(data),
                domain=None,
                twitter_share=None,
                facebook_share=None,
                title=None,
                date_published=None,
                pinterest_share=None,
                creator_name=None,
                creator_identifier=None,
                duration=None,
                facebook_comment=None,
                youtube_watch=None,
                youtube_like=None,
                youtube_comment=None,
                tiktok_share=None,
                tiktok_comment=None,
                reddit_engagement=None,
            )
