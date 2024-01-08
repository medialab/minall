# minall/enrichment/crowdtangle/normalizer.py

"""Module contains functions and dataclasses to normalize minet's CrowdTangle API client result.
"""

from dataclasses import dataclass
from typing import Dict, Generator, Optional

from casanova import TabularRecord
from minet.crowdtangle.types import CrowdTanglePost


def parse_shared_content(
    url: str, result: CrowdTanglePost
) -> Generator[Dict, None, None]:
    """Generator that streams the "media" attribute from minet's CrowdTanglePost object and returns normalized data as CSV dict row.

    Args:
        url (str): Target Facebook URL.
        result (CrowdTanglePost): minet's CrowdTangle API client result object.

    Yields:
        Generator[Dict, None, None]: Formatted CSV dict row of normalized shared content data.
    """
    if result and isinstance(getattr(result, "media"), list):
        for media in result.media:
            formatted_result = NormalizedSharedContent.from_payload(
                url=url, media=media
            )
            yield formatted_result.as_csv_dict_row()


def parse_facebook_post(url: str, result: CrowdTanglePost | None) -> Dict:
    """Transform minet's CrowdTanglePost object into normalized data as CSV dict row.

    Args:
        url (str): Target Facebook URL.
        result (CrowdTanglePost | None): If CrowdTangle API returned a match, minet's CrowdTangle API result object.

    Returns:
        Dict: Normalized data for Facebook post.
    """
    if result:
        formatted_result = NormalizedFacebookPost.from_payload(url, result)
        return formatted_result.as_csv_dict_row()
    else:
        return {"url": url, "domain": "facebook.com", "work_type": "SocialMediaPosting"}


@dataclass
class NormalizedSharedContent(TabularRecord):
    """Dataclass for normalizing data about media content shared in a Facebook post.

    Attributes:
        post_url (str): Target Facebook URL, which shared the media content.
        content_url (str): CrowdTangle's URI for the shared media.
        media_type (str): Ontological subtype for the shared media, i.e. "ImageObject".
        height (int | None): If available, the height in pixels of the shared media.
        width (int | None): If available, the width in pixels of the shared media.
    """

    post_url: str
    content_url: str | None
    media_type: str
    height: int | None
    width: int | None

    @classmethod
    def parse_media_type(cls, type: str | None) -> str:
        """Helper function to transform CrowdTangle's media classification into Schema.org's CreativeWork subtype.

        Args:
            type (str | None): If available, CrowdTangle's classification of the media object.

        Returns:
            str: Schema.org's CreativeWork subtype.
        """
        if type == "photo":
            return "ImageObject"
        elif type == "video":
            return "VideoObject"
        else:
            return "MediaObject"

    @classmethod
    def from_payload(
        cls,
        url: str,
        media: dict,
    ) -> "NormalizedSharedContent":
        """Parses JSON data in CrowdTanglePost's "media" attribute.

        Args:
            url (str): URL of Facebook post that contains shared media.
            media (dict): JSON in CrowdTanglePost's "media" attribute.

        Returns:
            NormalizedSharedContent: Dataclass that normalizes information about Facebook post's shared media content.
        """
        return NormalizedSharedContent(
            post_url=url,
            content_url=media.get("url"),
            media_type=cls.parse_media_type(media.get("type")),
            height=media.get("height"),
            width=media.get("width"),
        )


@dataclass
class NormalizedFacebookPost(TabularRecord):
    """Dataclass to normalize minet's CrowdTangle API result for Facebook posts.

    Attributes:
        url (str): Target Facebook URL.
        work_type (str): Target Facebook content's ontological subtype, i.e. "SocialMediaPosting", "ImageObject", "VideoObject".
        duration (str): If a Facebook content is a video, the video's duration.
        identifier (str): Facebook's identifier for the post.
        date_published (str): Date of teh Facebook post's publication.
        date_modified (str): Date when the Facebook post was last modified.
        title (str): If applicable, title of the Facebook post content.
        abstract (str): If applicable, description of the Facebook post content.
        text (str): If applicable, text of Facebook post content.
        creator_identifier (str): Facebook's identifier for the post's creator.
        creator_name (str): Name of entity responsible for the Facebook post publication.
        creator_location_created (str): If available, principal country in which is located the entity responsible for the post's publication.
        creator_url (str): URL for the entity responsible for the Facebook post's publication.
        creator_facebook_subscribe (int): Number of Facebook accounts subscribed to the account of the entity responsible for the Facebook post's publication.
        facebook_comment (int): Number of comments on the Facebook post.
        facebook_like (int): Number of Facebook accounts that have liked the Facebook post.
        facebook_share (int): Number of times the Facebook post has been shared on Facebook.
        domain (str): Domain for the Facebook post's URL. Default = "facebook.com".
        creator_type (str): Ontological subtype for the Facebook post's creator. Default = "defacto:SocialMediaAccount".
    """

    url: str
    work_type: str
    duration: str
    identifier: str
    date_published: str
    date_modified: str
    title: Optional[str]
    abstract: Optional[str]
    text: Optional[str]
    creator_identifier: str
    creator_name: str
    creator_location_created: Optional[str]
    creator_url: str
    creator_facebook_subscribe: int
    facebook_comment: int
    facebook_like: int
    facebook_share: int
    domain: str = "facebook.com"
    creator_type: str = "defacto:SocialMediaAccount"

    @classmethod
    def from_payload(
        cls,
        url: str,
        result: CrowdTanglePost,
    ) -> "NormalizedFacebookPost":
        """Parses minet's CrowdTangle result and creates normalized dataclass.

        Args:
            url (str): Target Facebook URL.
            result (CrowdTanglePost): Result object returned from minet's CrowdTangle API client.

        Returns:
            NormalizedFacebookPost: Dataclass that normalizes minet's CrowdTangle data.
        """
        work_type = "SocialMediaPosting"
        if hasattr(result, "type"):
            if result.type == "photo":
                work_type = "ImageObject"
            elif result.type == "video":
                work_type = "VideoObject"

        return NormalizedFacebookPost(
            url=url,
            work_type=work_type,
            duration=result.video_length_ms,
            identifier=result.id,
            date_published=result.date,
            date_modified=result.updated,
            title=result.title,
            abstract=result.description,
            text=result.message,
            creator_identifier=result.account.id,
            creator_facebook_subscribe=result.account.subscriber_count,
            creator_name=result.account.name,
            creator_location_created=result.account.page_admin_top_country,
            creator_url=result.account.url,
            facebook_comment=result.actual_comment_count,
            facebook_like=result.actual_like_count,
            facebook_share=result.actual_share_count,
        )
