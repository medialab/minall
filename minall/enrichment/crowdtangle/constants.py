from dataclasses import dataclass

from casanova import TabularRecord
from minet.crowdtangle.formatters import CrowdTanglePost


@dataclass
class NormalizedSharedContent(TabularRecord):
    post_url: str
    content_url: str | None
    media_type: str
    height: int | None
    width: int | None

    @classmethod
    def parse_media_type(cls, type: str | None) -> str:
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
        return NormalizedSharedContent(
            post_url=url,
            content_url=media.get("url"),
            media_type=cls.parse_media_type(media.get("type")),
            height=media.get("height"),
            width=media.get("width"),
        )


@dataclass
class NormalizedFacebookPost(TabularRecord):
    url: str
    work_type: str
    duration: str
    identifier: str
    date_published: str
    date_modified: str
    title: str
    abstract: str
    text: str
    creator_identifier: str
    creator_name: str
    creator_location_created: str
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
            creator_identifier=result.account_id,
            creator_facebook_subscribe=result.account_subscriber_count,
            creator_name=result.account_name,
            creator_location_created=result.account_page_admin_top_country,
            creator_url=result.account_url,
            facebook_comment=result.actual_comment_count,
            facebook_like=result.actual_like_count,
            facebook_share=result.actual_share_count,
        )
