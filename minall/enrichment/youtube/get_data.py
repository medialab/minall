# minall/enrichment/youtube/get_data.py

"""Module contains function to manage process of collecting and normalizing data about YouTube web content.
"""

from pathlib import Path

from minet.youtube.client import YouTubeAPIClient
from ural.youtube import YoutubeShort, YoutubeVideo

from minall.enrichment.youtube.context import ProgressBar, Writer
from minall.enrichment.youtube.normalizer import ParsedLink, normalize


def get_youtube_data(data: list[str], keys: list[str], outfile: Path) -> None:
    """Collects and writes metadata about target YouTube videos and channels to a CSV file that will be inserted into 'links' SQL table.

    Args:
        data (list[str]): Set of target YouTube URLs.
        keys (list[str]): Set of keys for YouTube API.
        outfile (Path): Path to CSV file for 'links' SQL table.
    """
    # Sort the URLs into channels and videos
    parsed_links = [ParsedLink(url) for url in data]
    n_videos = len(
        [
            i
            for i in parsed_links
            if isinstance(i.type, YoutubeVideo) or isinstance(i.type, YoutubeShort)
        ]
    )

    client = YouTubeAPIClient(key=keys)

    # Mutate the parsed_links array by adding video data
    with ProgressBar() as progress:
        t = progress.add_task(
            description="[bold red]Querying YouTube videos", total=n_videos
        )
        for pl in parsed_links:
            if isinstance(pl.type, YoutubeVideo) or isinstance(pl.type, YoutubeShort):
                for _, result in client.videos(videos=[pl.video_id]):
                    setattr(pl, "video_result", result)
                    setattr(pl, "channel_id", getattr(result, "channel_id") if result is not None else None)
                    progress.advance(t)

    # Get a unique set of channels from video and channel data
    channel_set = set()
    for pl in parsed_links:
        if pl.channel_id:
            channel_set.add("https://www.youtube.com/channel/" + pl.channel_id)

    # Create an index of unique channels and their collected metadata
    channel_index = {}
    with ProgressBar() as progress:
        t = progress.add_task(
            description="[bold red]Querying YouTube channels", total=len(channel_set)
        )
        for channel_url, result in client.channels(channels_target=channel_set):
            channel_id = channel_url.split("/")[-1]
            channel_index.update({channel_id: result})
            progress.advance(t)

    # Again mutate the parsed_links array by adding channel data
    for pl in parsed_links:
        if pl.channel_id:
            pl.channel_result = channel_index.get(pl.channel_id)

    with Writer(links_file=outfile) as writer:
        for pl in parsed_links:
            normalized_result = normalize(pl)
            writer.writerow(normalized_result)
