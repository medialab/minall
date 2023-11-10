from minet.youtube.types import YouTubeChannel as MinetYouTubeChannelResult
from minet.youtube.types import YouTubeVideo as MinetYouTubeVideoResult

from minall.enrichment.youtube.constants import (
    NormalizedYouTubeChannel,
    NormalizedYouTubeVideo,
    ParsedLink,
)


def normalize(parsed_link: ParsedLink) -> dict:
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
