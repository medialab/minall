# minall/enrichment/youtube/normalizer.py

"""Module contains dataclasses to normalize minet's YouTube Video and Channel result objects.
"""

from dataclasses import dataclass
from typing import List

from casanova import TabularRecord
from minet.youtube.types import YouTubeChannel as MinetYouTubeChannelResult
from minet.youtube.types import YouTubeVideo as MinetYouTubeVideoResult
from ural.youtube import YoutubeChannel, YoutubeVideo, parse_youtube_url


class ParsedLink:
    """Class to store up-to-date metadata about target YouTube URL.

    This class's instance variables will be updated during the data collection process to reflect the target URL's video and/or channel metadata. If the target URL is of a video, its `ParsedLink` class instance should eventually be mutated to have a value in both the `video_result` and `channel_result` attributes because 2 API calls will be made. If the target URL is of a channel, its `ParsedLink` class instance should eventually be mutated to have a value in the `channel_result` attribute, after 1 call to the YouTube API's channels endpoint.
    """

    def __init__(self, url: str) -> None:
        """Determine type of YouTube web content.

        Args:
            url (str): Target YouTube URL.

        Attributes:
            link_id (str): Target YouTube URL.
            type (YoutubeChannel | YoutubeVideo | Any): Result of ural's `parse_youtube_url()` function.
            video_id (str | None): If a parsed YouTube type is a video, the result's `id` attribute.
            channel_id (str | None): If a parsed YouTube type is a channel, the result's `id` attribute.
            video_result (None): Empty class instance variable for later storing minet's video result object.
            channel_result (None): Empty class instance variable for later storing minet's channel result object.
        """
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


def normalize(parsed_link: ParsedLink) -> dict:
    """Normalize minet result objects stored in instance variables of the `ParsedLink` class.

    Args:
        parsed_link (ParsedLink): Class instance with minet's YouTube API results.

    Returns:
        dict: Dictionary to be added to CSV row for 'links' SQL table.
    """

    url = parsed_link.link_id
    if isinstance(parsed_link.video_result, MinetYouTubeVideoResult):
        data = NormalizedYouTubeVideo.from_payload(
            url=url,
            channel_result=parsed_link.channel_result,
            video_result=parsed_link.video_result,
        )
        return data.as_csv_dict_row()
    elif isinstance(parsed_link.channel_result, MinetYouTubeChannelResult):
        data = NormalizedYouTubeChannel.from_payload(
            url=url, channel_result=parsed_link.channel_result
        )
        return data.as_csv_dict_row()
    else:
        return {"url": url}


@dataclass
class NormalizedYouTubeVideo(TabularRecord):
    """Dataclass to normalize minet's YoutubeVideo result object.

    Attributes:
        url (str): Target YouTube video URL.
        identifier (str): YouTube's unique identifier for the video.
        date_published (str): Date the video was published on YouTube.
        duration (str): Duration of the video.
        title (str): Title of the video.
        abstract (str): Video's description.
        keywords (List): List of keywords applied to video.
        youtube_watch (str): Number of users who have watched the YouTube video.
        youtube_comment (str): Number of users who have commented on the YouTube video.
        youtube_like (str): Number of users who have liked the YouTube video.
        creator_type (str): Ontological subtype of the video's channel.
        creator_name (str): Name of the video's channel.
        creator_date_created (str): Date when the video's channel was created.
        creator_location_created (str): Primary country in which the video's channel publishes content.
        creator_identifier (str): YouTube's unique identifier for the video's channel.
        creator_youtube_subscribe (str): Number of YouTube accounts that subscribe to the video's channel.
        creator_create_video (str): Number of videos the video's channel has published.
        domain (str): Domain of target URL. Default = "youtube.com".
        work_type (str): Ontological subtype of target web content. Default = "VideoObject".
    """

    url: str
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
    domain: str = "youtube.com"
    work_type: str = "VideoObject"

    @classmethod
    def from_payload(
        cls,
        url: str,
        channel_result: MinetYouTubeChannelResult | None,
        video_result: MinetYouTubeVideoResult,
    ) -> "NormalizedYouTubeVideo":
        """Parses minet's data for both a video and channel and creates a normalized dataclass.

        Args:
            url (str): Target YouTube video URL.
            channel_result (MinetYouTubeChannelResult | None): minet's channel results containing metadata about the target video's channel.
            video_result (MinetYouTubeVideoResult): minet's video results for the target video.

        Returns:
            NormalizedYouTubeVideo: Dataclass that normalizes and merges video and channel results.
        """
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
    """Dataclass to normalize minet's YoutubeChannel result object.

    Attributes:
        url (str): Target YouTube channel URL.
        identifier (str): YouTube's unique identifier for the channel.
        date_published (str): Date when the channel was created.
        country_of_origin (str): Primary country in which the channel publishes content.
        title (str): Name of the channel.
        abstract (str): Description of the channel.
        keywords (List[str]): List of keywords attributed to the channel.
        youtube_subscribe (int): Number of YouTube users who subscribe to the channel.
        create_video (int): Number of videos the channel has published.
        domain (str): Domain of target URL. Default = "youtube.com".
        work_type (str): Ontological subtype of target web content. Default = "WebPage".
    """

    url: str
    identifier: str
    date_published: str
    country_of_origin: str
    title: str
    abstract: str
    keywords: List[str]
    youtube_subscribe: int
    create_video: int
    domain: str = "youtube.com"
    work_type: str = "WebPage"

    @classmethod
    def from_payload(
        cls,
        url: str,
        channel_result: MinetYouTubeChannelResult,
    ) -> "NormalizedYouTubeChannel":
        """Parses minet's channel result and creates a normalized dataclass.

        Args:
            url (str): Target YouTube channel URL.
            channel_result (MinetYouTubeChannelResult): minet's channel results for the target channel URL.

        Returns:
            NormalizedYouTubeChannel: Dataclass that normalizes minet's channel results.
        """
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
