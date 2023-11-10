from dataclasses import dataclass
from typing import List

from casanova import TabularRecord
from minet.youtube.types import YouTubeChannel as MinetYouTubeChannelResult
from minet.youtube.types import YouTubeVideo as MinetYouTubeVideoResult
from ural.youtube import YoutubeChannel, YoutubeVideo, parse_youtube_url


class ParsedLink:
    def __init__(self, url: str) -> None:
        self.link_id = url

        self.type = parse_youtube_url(url)

        if isinstance(self.type, YoutubeVideo):
            self.video_id = getattr(self.type, "id")
            self.channel_id = None

        elif isinstance(self.type, YoutubeChannel):
            self.channel_id = getattr(self.type, "id")
            self.video_id = None

        self.video_result = None
        self.channel_result = None


@dataclass
class NormalizedYouTubeVideo(TabularRecord):
    url: str
    domain: str
    work_type: str
    identifier: str
    date_published: str
    duration: str
    title: str
    abstract: str
    keywords: List[str]
    youtube_watch: str
    youtube_comment: str
    youtube_like: str
    # youtube_favorite was depreciated by YouTube in 2015.
    creator_type: str
    creator_name: str
    creator_date_created: str
    creator_location_created: str
    creator_identifier: str
    creator_youtube_subscribe: str
    creator_create_video: str

    @classmethod
    def from_payload(
        cls,
        url: str,
        channel_result: MinetYouTubeChannelResult | None,
        video_result: MinetYouTubeVideoResult,
    ) -> "NormalizedYouTubeVideo":
        if channel_result:
            channel = channel_result.as_csv_dict_row()
        else:
            channel = {}
        return NormalizedYouTubeVideo(
            url=url,
            domain="youtube.com",
            work_type="VideoObject",
            identifier=video_result.video_id,
            date_published=video_result.published_at,
            duration=video_result.duration,
            title=video_result.title,
            abstract=video_result.description,
            keywords=channel.get("keywords"),  # type: ignore
            youtube_watch=video_result.view_count,  # type: ignore
            youtube_comment=video_result.comment_count,  # type: ignore
            youtube_like=video_result.like_count,  # type: ignore
            creator_type="WebPage",
            creator_name=video_result.channel_title,
            creator_identifier=video_result.channel_id,
            creator_date_created=channel.get("published_at"),  # type: ignore
            creator_location_created=channel.get("country"),  # type: ignore
            creator_youtube_subscribe=channel.get("subscriber_count"),  # type: ignore
            creator_create_video=channel.get("video_count"),  # type: ignore
        )


@dataclass
class NormalizedYouTubeChannel(TabularRecord):
    url: str
    domain: str
    work_type: str
    identifier: str
    date_published: str
    country_of_origin: str
    title: str
    abstract: str
    keywords: List[str]
    youtube_subscribe: int
    create_video: int

    @classmethod
    def from_payload(
        cls,
        url: str,
        channel_result: MinetYouTubeChannelResult,
    ) -> "NormalizedYouTubeChannel":
        return NormalizedYouTubeChannel(
            url=url,
            domain="youtube.com",
            work_type="WebPage",
            identifier=channel_result.channel_id,
            date_published=channel_result.published_at,
            country_of_origin=channel_result.country,
            title=channel_result.title,
            abstract=channel_result.description,
            keywords=channel_result.keywords,
            youtube_subscribe=channel_result.subscriber_count,
            create_video=channel_result.video_count,
        )
