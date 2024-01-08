# minall/enrichment/buzzsumo/client.py

"""Module containing a wrapper for minet's Buzzsumo API client.
"""

from minet.buzzsumo.client import BuzzSumoAPIClient

from minall.enrichment.buzzsumo.normalizer import (
    BEGINDATE,
    ENDDATE,
    NormalizedBuzzsumoResult,
)


class BuzzsumoClient:
    """Wrapper for minet's Buzzsumo API client.

    Examples:
        >>> import os
        >>> wrapper = BuzzsumoClient(token=os.environ["BUZZSUMO_TOKEN"])
        >>> url="https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/"
        >>> wrapper(url)
        NormalizedBuzzsumoResult(url='https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/', work_type='Article', domain='fosdem.org', twitter_share=0, facebook_share=0, title='FOSDEM 2020 - Empowering social scientists with web mining tools', date_published=datetime.datetime(2024, 1, 4, 15, 48, 1), pinterest_share=0, creator_name=None, creator_identifier=None, duration=None, facebook_comment=0, youtube_watch=None, youtube_like=None, youtube_comment=None, tiktok_share=None, tiktok_comment=None, reddit_engagement=0)
    """

    def __init__(self, token: str) -> None:
        """Creates an instance of mient's BuzzsumoAPIClient and sets values for the Buzzsumo API's requried begin-date and end-date parameters.

        Examples:
            >>> wrapper = BuzzsumoClient(token="<TOKEN>")
            >>> type(wrapper)
            <class 'minall.enrichment.buzzsumo.client.BuzzsumoClient'>
            >>> type(wrapper.client)
            <class 'minet.buzzsumo.client.BuzzSumoAPIClient'>

        Args:
            token (str): Buzzsumo API token.
        """
        self.client = BuzzSumoAPIClient(token=token)
        self.begin = BEGINDATE
        self.end = ENDDATE

    def __call__(self, url: str) -> NormalizedBuzzsumoResult:
        """Executes mient's Buzzsumo API client on a URL and returns normalized data.

        Args:
            url (str): Target URL.

        Returns:
            NormalizedBuzzsumoResult: Dataclass that normalizes minet's Buzzsumo result.
        """
        result = self.client.exact_url(
            search_url=url, begin_timestamp=self.begin, end_timestamp=self.end
        )
        return NormalizedBuzzsumoResult.from_payload(url, result)
