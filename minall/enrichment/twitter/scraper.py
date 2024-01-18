# minall/enrichments/twitter/scraper.py

"""Module contains TweetScraper wrapper for setting up and calling the minet TweetGuestAPIScraper"""

from typing import Dict, Tuple

from minet.twitter import TwitterGuestAPIScraper
from ural.twitter import TwitterTweet, parse_twitter_url


class TweetScraper:
    """Wrapper for running minet's Tweet Guest API Scraper.

    Examples:
        >>> scraper = TweetScraper()
        >>>
        >>> tweet_url = "https://twitter.com/Paris2024/status/1551605445156012038"
        >>>
        >>> url, tweet = scraper(tweet_url)
        >>>
        >>> url
        'https://twitter.com/Paris2024/status/1551605445156012038'
        >>>
        >>> tweet["local_time"]
        '2022-07-25T16:29:00'
    """

    def __init__(self) -> None:
        """Set up minet's Twitter Guest API Scraper"""

        self.scraper = TwitterGuestAPIScraper()

    def __call__(self, url: str) -> Tuple[str, Dict | None]:
        """If the URL is of a Tweet and the ID can be parsed, scrape and return data.

        Args:
            url (str): URL of Tweet.

        Returns:
            Tuple[str, Dict | None]: If data could be scraped, the target URL and the data; otherwise the unsuccessful URL and None.
        """
        result = None
        parsed_url = parse_twitter_url(url)
        if isinstance(parsed_url, TwitterTweet):
            tweet_id = getattr(parsed_url, "id")
            if tweet_id is not None:
                try:
                    result = self.scraper.tweet(tweet_id)
                except Exception:
                    pass
        return url, result
