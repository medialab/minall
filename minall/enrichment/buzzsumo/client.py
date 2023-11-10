from typing import Tuple

from minet.buzzsumo.client import BuzzSumoAPIClient
from minet.buzzsumo.types import BuzzsumoArticle

from minall.enrichment.buzzsumo.constants import BEGINDATE, ENDDATE


class BuzzsumoCommand:
    def __init__(self, token: str) -> None:
        self.client = BuzzSumoAPIClient(token=token)
        self.begin_date = BEGINDATE
        self.end_date = ENDDATE

    def __call__(self, url: str) -> Tuple[str, BuzzsumoArticle | None]:
        # Call minet's Buzzsumo client method
        return url, self.client.exact_url(
            search_url=url, begin_timestamp=self.begin_date, end_timestamp=self.end_date
        )
