import csv
from pathlib import Path

from ural.youtube import YoutubeChannel, YoutubeVideo, parse_youtube_url

from minall.enrichment.youtube.client import YoutubeCommands
from minall.enrichment.youtube.constants import (
    MinetResult,
    ParsedChannelLink,
    ParsedVideoLink,
    YoutubeResults,
)
from minall.enrichment.youtube.normalizer import YoutubeNormalizer
from minall.links.constants import LINKS_FIELDNAMES
from minall.utils import progress_bar


def get_youtube_data(data: list[tuple[str, str]], keys: list[str], outfile: Path):
    # Sort the data into channels and videos
    parsed_links = [(url, review_id, parse_youtube_url(url)) for url, review_id in data]
    channel_links = [
        ParsedChannelLink(url=url, link_id=link_id, id=getattr(parsed_link, "id"))
        for url, link_id, parsed_link in parsed_links
        if isinstance(parsed_link, YoutubeChannel)
        and getattr(parsed_link, "id") is not None
    ]
    video_links = [
        ParsedVideoLink(url=url, link_id=link_id, id=getattr(parsed_link, "id"))
        for url, link_id, parsed_link in parsed_links
        if isinstance(parsed_link, YoutubeVideo)
        and getattr(parsed_link, "id") is not None
    ]

    # Set up minet's YouTube API client
    client = YoutubeCommands(keys=keys)

    # Collect videos' metadata, recovering also their channel ID
    combined_results = {}
    with progress_bar() as progress:
        t = progress.add_task(description="[red]YouTube Videos", total=len(video_links))
        for video in client.videos(video_links):
            # From parsed video metadata, add newly discovered channel IDs
            # to the list of channel links
            if video and video.id not in [channel.id for channel in channel_links]:
                channel_links.append(
                    ParsedChannelLink(
                        url=video.url,
                        link_id=video.link_id,
                        id=getattr(video.result, "channel_id"),
                    )
                )
            parse_result(
                result=video, combined_results=combined_results, target="video"
            )
            progress.advance(t)

    # Collect channels' metadata
    with progress_bar() as progress:
        t = progress.add_task(
            description="[red]YouTube Channels", total=len(channel_links)
        )
        for channel in client.channels(channel_links):
            parse_result(
                result=channel, combined_results=combined_results, target="channel"
            )
            progress.advance(t)

    # Combine all the video and channel data
    all_youtube_data = parse_combined_results(combined_results)

    # Set up a normalizer
    normalizer = YoutubeNormalizer()

    # Normalize and write the results to the appearances outfile
    print(f"\n\tWriting YouTube results to '{outfile}'")
    with open(outfile, "w") as f:
        writer = csv.DictWriter(f, fieldnames=LINKS_FIELDNAMES)
        writer.writeheader()
        for data in all_youtube_data:  # type: ignore
            result = normalizer(data=data)  # type: ignore
            writer.writerow(result)


def parse_result(result: MinetResult, combined_results: dict, target: str):
    if not combined_results.get(result.url):
        combined_results.update(
            {
                result.url: {
                    "link_id": set(),
                    "video_result": None,
                    "channel_result": None,
                }
            }
        )
    combined_results[result.url]["link_id"].add(result.link_id)
    combined_results[result.url][f"{target}_result"] = result.result


def parse_combined_results(combined_results: dict) -> list[MinetResult]:
    exploded_results = []
    for url, related_data in combined_results.items():
        for link_id in related_data.get("link_id"):
            exploded_results.append(
                YoutubeResults(
                    url=url,
                    link_id=link_id,
                    video=related_data.get("video_result"),
                    channel=related_data.get("channel_result"),
                )
            )
    return exploded_results
