from minet.buzzsumo.client import BuzzSumoAPIClient

from minall.enrichment.buzzsumo.constants import (
    BEGINDATE,
    ENDDATE,
    NormalizedBuzzsumoResult,
)


class BuzzsumoClient:
    def __init__(self, token: str) -> None:
        self.client = BuzzSumoAPIClient(token=token)
        self.begin = BEGINDATE
        self.end = ENDDATE

    def __call__(self, url: str) -> NormalizedBuzzsumoResult:
        result = self.client.exact_url(
            search_url=url, begin_timestamp=self.begin, end_timestamp=self.end
        )
        return NormalizedBuzzsumoResult.from_payload(url, result)
