import csv
from pathlib import Path

from minet.youtube.client import YouTubeAPIClient
from ural.youtube import YoutubeChannel, YoutubeVideo

from minall.enrichment.youtube.constants import ParsedLink
from minall.enrichment.youtube.context import ProgressBar, Writer
from minall.enrichment.youtube.normalizer import normalize


def get_youtube_data(data: list[str], keys: list[str], outfile: Path) -> None:
    # Sort the URLs into channels and videos
    parsed_links = [ParsedLink(url) for url in data]
    n_videos = len([i for i in parsed_links if isinstance(i.type, YoutubeVideo)])

    client = YouTubeAPIClient(key=keys)

    # Mutate the parsed_links array by adding video data
    with ProgressBar() as progress:
        t = progress.add_task(
            description="[bold red]Querying YouTube videos", total=n_videos
        )
        for pl in parsed_links:
            if isinstance(pl.type, YoutubeVideo):
                for _, result in client.videos(videos=[pl.video_id]):
                    setattr(pl, "video_result", result)
                    setattr(pl, "channel_id", getattr(result, "channel_id"))
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
