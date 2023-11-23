import itertools
import os
import unittest
from datetime import datetime
from typing import List

from ebbe import Timer
from minet.buzzsumo.client import BuzzSumoAPIClient
from rich import print
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

BEGINDATE = int(datetime.strptime("2020-01-01", "%Y-%m-%d").timestamp())

ENDDATE = int(
    datetime.strptime(
        datetime.utcnow().isoformat().split("T")[0], "%Y-%m-%d"
    ).timestamp()
)

# URL that Buzzsumo API has indexed
DATA = [
    "https://www.lemonde.fr/idees/article/2023/10/23/maintenir-la-pression-pour-lutter-contre-l-evasion-fiscale_6196088_3232.html",
    "https://www.youtube.com/watch?v=bj6PcWBgVN4",
    "https://twitter.com/patateMiDouce/status/1724737737029239202",
    "https://planetes360.fr/attention-multiplication-par-5-des-deces-cardiaques-soudains-chez-les-joueurs-de-la-fifa-en-2021/",
    "https://www.francesoir.fr/politique-monde/robert-malone-plaidoyer-vaccination-enfants",
    "https://www.france.tv/france-5/c-dans-l-air/3071975-special-presidentielle-marine-le-pen-et-fabien-roussel.html",
]

N_DUPLICATES = 5


def duplicate_examples(data: List[str]) -> List[str]:
    return list(
        itertools.chain.from_iterable(
            [list(itertools.repeat(d, N_DUPLICATES)) for d in DATA]
        )
    )


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.token = os.environ["BUZZSUMO_TOKEN"]
        self.client = BuzzSumoAPIClient(token=self.token)
        self.data = duplicate_examples(DATA)
        self.url_without_result = (
            "https://twitter.com/patateMiDouce/status/1724737737029239202"
        )
        self.progress_bar = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )

    def test_loop(self) -> None:
        # Affirm the token isn't None
        token = self.token
        assert token

        with Timer(), self.progress_bar as p:
            t = p.add_task("Call Buzzsumo API", total=len(self.data))

            # Set up print for showing which URL is taking time
            current_url = None
            for url in self.data:
                if url != current_url:
                    print(Panel.fit(f"Testing URL: '{url}'"))
                    current_url = url

                # Call minet's Buzzsumo API client
                result = self.client.exact_url(
                    search_url=url, end_timestamp=ENDDATE, begin_timestamp=BEGINDATE
                )

                # Advance the progress bar and assert known matches aren't None
                p.advance(t)
                if not url == self.url_without_result:
                    self.assertIsNotNone(getattr(result, "title"))


if __name__ == "__main__":
    unittest.main()
