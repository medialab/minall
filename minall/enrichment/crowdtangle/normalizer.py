import csv
import json

from casanova import namedrecord

from minall.enrichment.crowdtangle.constants import CrowdTangleResult
from minall.links.constants import LINKS_FIELDNAMES
from minall.shared_content.constants import SHARED_CONTENT_FIELDNAMES


class FacebookPostNormalizer:
    def __init__(self) -> None:
        self.record = namedrecord(
            "Record",
            fields=LINKS_FIELDNAMES,
            defaults=[None for _ in range(len(LINKS_FIELDNAMES))],
        )

    def __call__(self, data: dict, link_id: str, url: str) -> dict:
        keep = {
            "link_id": link_id,
            "url": url,
            "domain": "facebook.com",
            "type": "SocialMediaPosting",
            "duration": data.get("video_length_ms"),
            "identifier": data.get("id"),
            "date_published": data.get("date"),
            "date_modified": data.get("updated"),
            "abstract": data.get("description"),
            "text": data.get("message"),
            "title": data.get("title"),
            "creator_type": "defacto:SocialMediaAccount",
            "creator_identifier": data.get("account_id"),
            "creator_facebook_subscribe": data.get("account_subscriber_count"),
            "creator_name": data.get("account_name"),
            "creator_location_created": data.get("account_page_admin_top_country"),
            "creator_url": data.get("account_url"),
            "facebook_comment": data.get("actual_comment_count"),
            "facebook_like": data.get("actual_like_count"),
            "facebook_share": data.get("actual_share_count"),
        }

        return self.record(**keep).as_csv_dict_row()


class SharedContentNormalizer:
    def __init__(self) -> None:
        self.record = namedrecord(
            "Record",
            fields=SHARED_CONTENT_FIELDNAMES,
            defaults=[None for _ in range(len(SHARED_CONTENT_FIELDNAMES))],
        )

    def parse_media_type(self, type: str | None) -> str:
        if type == "photo":
            return "ImageObject"
        elif type == "video":
            return "VideoObject"
        else:
            return "MediaObject"

    def __call__(
        self,
        data: dict,
        post_url: str,
    ) -> dict:
        keep = {
            "post_url": post_url,
            "type": self.parse_media_type(data.get("type")),
            "content_url": data.get("url"),
            "height": data.get("height"),
            "width": data.get("width"),
        }

        return self.record(**keep).as_csv_dict_row()


class ResultParser:
    def __init__(
        self, links_writer: csv.DictWriter, shared_content_writer: csv.DictWriter
    ) -> None:
        self.links_writer = links_writer
        self.shared_content_writer = shared_content_writer
        self.links_normalizer = FacebookPostNormalizer()
        self.shared_content_normalizer = SharedContentNormalizer()

    def __call__(self, result: CrowdTangleResult):
        if result.FacebookPost is not None:
            # Write the post's metadata for the appearance
            post_dict_data = result.FacebookPost.as_csv_dict_row()
            reformatted_row = self.links_normalizer(
                data=post_dict_data, link_id=result.link_id, url=result.url
            )
            self.links_writer.writerow(reformatted_row)

            # If the post shared media, parse and write each one
            shared_media_json_string = post_dict_data.get("media")
            facebook_appearance_url = result.url
            if (
                facebook_appearance_url
                and shared_media_json_string
                and shared_media_json_string != ""
            ):
                try:
                    shared_media = json.loads(shared_media_json_string)
                except json.JSONDecodeError as e:
                    print(e)
                else:
                    if isinstance(shared_media, list):
                        for media in shared_media:
                            content_dict = self.shared_content_normalizer(
                                data=media,
                                post_url=facebook_appearance_url,
                            )
                            self.shared_content_writer.writerow(content_dict)
