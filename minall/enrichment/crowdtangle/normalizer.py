from typing import Dict, Generator

from minet.crowdtangle.formatters import CrowdTanglePost

from minall.enrichment.crowdtangle.constants import (
    NormalizedFacebookPost,
    NormalizedSharedContent,
)


def parse_shared_content(url, result) -> Generator[Dict, None, None]:
    if result and isinstance(getattr(result, "media"), list):
        for media in result.media:
            formatted_result = NormalizedSharedContent.from_payload(
                url=url, media=media
            )
            yield formatted_result.as_csv_dict_row()


def parse_facebook_post(url: str, result: CrowdTanglePost | None) -> Dict:
    if result:
        formatted_result = NormalizedFacebookPost.from_payload(url, result)
        return formatted_result.as_csv_dict_row()
    else:
        return {"url": url, "domain": "facebook.com", "work_type": "SocialMediaPosting"}
