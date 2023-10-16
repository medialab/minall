from collections import namedtuple

ParsedVideoLink = namedtuple("ParsedVideoRecord", field_names=["url", "link_id", "id"])
ParsedChannelLink = namedtuple(
    "ParsedChannelRecord", field_names=["url", "link_id", "id"]
)
MinetResult = namedtuple("MinetResult", field_names=["url", "link_id", "id", "result"])
YoutubeResults = namedtuple(
    "YouTubeResults",
    field_names=["url", "link_id", "video", "channel"],
    defaults=[None for _ in range(4)],
)
