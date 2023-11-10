from typing import Generator

from minall.enrichment.crowdtangle.constants import (
    NormalizedFacebookPost,
    NormalizedSharedContent,
)


def parse_shared_content(url, result) -> Generator[dict, None, None]:
    if result and isinstance(getattr(result, "media"), list):
        for media in result.media:
            formatted_result = NormalizedSharedContent.from_payload(
                url=url, media=media
            )
            yield formatted_result.as_csv_dict_row()


def parse_facebook_post(url, result) -> dict | None:
    if result:
        formatted_result = NormalizedFacebookPost.from_payload(url, result)
        return formatted_result.as_csv_dict_row()
