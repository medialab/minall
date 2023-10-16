from typing import Generator

from minet.youtube.client import YouTubeAPIClient

from minall.enrichment.youtube.constants import (
    MinetResult,
    ParsedChannelLink,
    ParsedVideoLink,
)


class YoutubeCommands:
    def __init__(self, keys: list) -> None:
        self.client = YouTubeAPIClient(key=keys)

    def videos(self, data: list[ParsedVideoLink]) -> Generator[MinetResult, None, None]:
        for video in data:
            url = getattr(video, "url")
            link_id = getattr(video, "link_id")
            video_id = getattr(video, "id")
            for _, result in self.client.videos(videos=[video_id]):
                yield MinetResult(url=url, link_id=link_id, id=video_id, result=result)

    def channels(self, data: list[ParsedChannelLink]) -> Generator:
        for channel in data:
            url = getattr(channel, "url")
            link_id = getattr(channel, "link_id")
            channel_id = getattr(channel, "id")
            for _, result in self.client.channels(channels_target=[channel_id]):
                yield MinetResult(
                    url=url, link_id=link_id, id=channel_id, result=result
                )
