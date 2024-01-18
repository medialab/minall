# minall/enrichment/twitter/normalizer.py

"""Module contains constants for minet's Twitter Guest API Scraper and a dataclass to normalize minet's result.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Generator, List, Optional

from casanova import TabularRecord


@dataclass
class NormalizedTweet(TabularRecord):
    """Dataclass to normalize minet's Twitter API result.

    Attributes:
        url (str): Target URL of Tweet searched on Twitter.
        identifier (Optional[str]): Tweet ID. Default = None.
        date_published (Optional[datetime]): UTC timestamp of Tweet publication, parsed as DateTime object. Default = None.
        text (Optional[str]): Text of Tweet . Default = None.
        creator_date_created (Optional[datetime]): UTC timestamp of User account creation, parsed as DateTime object. Default = None.
        creator_identifier (Optional[str]): User account ID . Default = None.
        creator_twitter_follow (Optional[int]): Number of accounts that follow the User account that published the Tweet. Default = None.
        creator_name (Optional[str]): Name of the User account. Default = None.
        twitter_share (Optional[int]): Number of times the Tweet was retweeted. Default = None.
        twitter_like (Optional[int]): Number of times the Tweet was liked. Default = None.
        domain (Optional[str]): Domain name of the target URL. Default = "twitter.com".
        work_type (str): Target URL's ontological subtype. Default = "SocialMediaPosting".
        hashtags (List): Hashtags embedded in Tweet. Default = [].
        creator_type (str): Ontological subtype of the User account. Default = "defacto:SocialMediaAccount".
    """

    url: str
    identifier: Optional[str] = None
    date_published: Optional[datetime] = None
    text: Optional[str] = None
    creator_date_created: Optional[datetime] = None
    creator_identifier: Optional[str] = None
    creator_twitter_follow: Optional[int] = None
    creator_name: Optional[str] = None
    twitter_share: Optional[int] = None
    twitter_like: Optional[int] = None
    domain: str = "twitter.com"
    work_type: str = "SocialMediaPosting"
    hashtags: List = field(default_factory=lambda: [])
    creator_type: str = "defacto:SocialMediaAccount"

    @classmethod
    def from_payload(cls, url: str, tweet: Dict | None) -> "NormalizedTweet":
        if tweet:
            return NormalizedTweet(
                url=url,
                identifier=tweet["id"],
                date_published=datetime.fromtimestamp(tweet["timestamp_utc"]),
                text=tweet["text"],
                creator_date_created=datetime.fromtimestamp(
                    tweet["user_timestamp_utc"]
                ),
                creator_identifier=tweet["user_id"],
                creator_twitter_follow=tweet["user_followers"],
                creator_name=tweet["user_name"],
                twitter_share=tweet["retweet_count"],
                twitter_like=tweet["like_count"],
                hashtags=tweet["hashtags"],
            )
        else:
            return NormalizedTweet(url=url)


@dataclass
class NormalizedSharedLink(TabularRecord):
    """Dataclass to normalized media embedded in Tweet.

    Attributes:
        post_url (str): URL of the Tweet in which the content is embedded.
        content_url (str): URL of the embedded content.
        media_type (str): Content URL's ontological subtype, i.e. "VideoObject".
        height (int | None): Height of the embedded visual media content. Default = None.
        width (int | None ): Width of the embedded visual media content. Default = None.
    """

    post_url: str
    content_url: str
    media_type: str
    height: int | None = None
    width: int | None = None


def parse_shared_content(
    url: str, tweet: Dict | None
) -> Generator[NormalizedSharedLink | None, None, None]:
    """Parse the potentially multiple media embedded in a Tweet and yield each one.

    Args:
        url (str): URL of Tweet with embedded media.
        tweet (Dict | None): Full metadata of Tweet.

    Yields:
        Generator[NormalizedSharedLink | None, None, None]: If media could be parsed, its normalized metadata.
    """
    if tweet:
        media_types = tweet.get("media_types")
        media_urls = tweet.get("media_urls")
        media_files = tweet.get("media_files")
        if (
            media_types
            and media_urls
            and media_files
            and len(media_files) == len(media_urls)
            and len(media_urls) == len(media_types)
        ):
            medias = list(zip(media_types, media_urls, media_files))
            for media_type, media_url, media_file in medias:
                if media_type == "video":
                    media_type = "VideoObject"
                elif media_type == "photo":
                    media_type = "ImageObject"
                else:
                    media_type = "MediaObject"
                yield NormalizedSharedLink(
                    post_url=url, content_url=media_url, media_type=media_type
                )
