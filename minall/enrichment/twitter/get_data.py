# minall/enrichment/twitter/get_data.py

"""Module contains functions for collecting, normalizing, and writing data from Twitter.
"""

from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from pathlib import Path
from typing import List

from minall.enrichment.crowdtangle.contexts import ContextManager
from minall.enrichment.twitter.normalizer import NormalizedTweet, parse_shared_content
from minall.enrichment.twitter.scraper import TweetScraper


def get_twitter_data(
    data: List[str],
    links_outfile: Path,
    shared_content_outfile: Path,
) -> None:
    """Transforms a set of Twitter URLs into collected Tweet metadata, written to CSV files.

    Args:
        data (List[str]): Set of Twitter ULRs.
        links_outfile (Path): Path to CSV file for Tweet metadata.
        shared_content_outfile (Path): Path to CSV file for metadata about links in Tweets.
    """
    with ContextManager(links_outfile, shared_content_outfile) as contexts:
        links_writer, shared_content_writer, progress = contexts

        t = progress.add_task(description="[bold blue]Querying Tweets", total=len(data))

        for batch in batched(data, 10):
            scraper = TweetScraper()
            with ThreadPoolExecutor() as executor:
                for url, tweet in executor.map(scraper, batch):
                    formatted_tweet = NormalizedTweet.from_payload(url=url, tweet=tweet)
                    links_writer.writerow(formatted_tweet.as_csv_dict_row())

                    # Write the shared content data
                    for shared_link in parse_shared_content(url=url, tweet=tweet):
                        if shared_link:
                            shared_content_writer.writerow(
                                shared_link.as_csv_dict_row()
                            )

                    progress.advance(t)


def batched(iterable, n):
    """Batch data into lists of length n. The last batch may be shorter.

    Function implemeneted in Python 3.12 itertools. Solution taken from Python issue at [https://github.com/python/cpython/issues/98363](https://github.com/python/cpython/issues/98363).
    """
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be >= 1")
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch
