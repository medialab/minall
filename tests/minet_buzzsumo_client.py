import itertools
import os
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from ebbe import Timer
from minet.buzzsumo.client import BuzzSumoAPIClient
from minet.buzzsumo.types import BuzzsumoArticle
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

single_thread_log = Path.cwd().joinpath("single.log")
mulithread_log = Path.cwd().joinpath("mulithread.log")


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


class ThreadedClient:
    def __init__(self, token: str, logfile) -> None:
        self.client = BuzzSumoAPIClient(token=token)
        self.open_logfile = logfile

    def __call__(self, url: str) -> Tuple[str, BuzzsumoArticle | None]:
        with Timer(file=self.open_logfile, name=f"Time for {url}"):
            result = self.client.exact_url(url, BEGINDATE, ENDDATE)
        return url, result


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
        self.threaded_client = ThreadedClient(token=self.token, logfile=None)

    def test_loop(self) -> None:
        # Affirm the token isn't None
        token = self.token
        assert token

        with open(single_thread_log, "w") as f:
            with Timer(
                file=f, name=f"Single-thread on {len(self.data)} URLs"
            ), self.progress_bar as p:
                task = p.add_task("Call Buzzsumo API", total=len(self.data))

                for url in self.data:
                    # Call minet's Buzzsumo API client
                    with Timer(file=f, name=f"Time for {url}"):
                        result = self.client.exact_url(
                            search_url=url,
                            begin_timestamp=BEGINDATE,
                            end_timestamp=ENDDATE,
                        )

                    # Advance the progress bar and assert known matches aren't None
                    p.advance(task)
                    if not url == self.url_without_result:
                        self.assertIsNotNone(getattr(result, "title"))

    def test_multithread(self) -> None:
        # Affirm the token isn't None
        token = self.token
        assert token

        with open(mulithread_log, "w") as f:
            self.threaded_client.open_logfile = f
            with Timer(
                file=f, name=f"Multi-thread on {len(self.data)} URLs"
            ), self.progress_bar as p, ThreadPoolExecutor() as executor:
                t = p.add_task("Call Buzzsumo API", total=len(self.data))

                for result in executor.map(self.threaded_client, self.data):
                    url, bz_result = result
                    # Advance the progress bar and assert known matches aren't None
                    p.advance(t)
                    if not url == self.url_without_result:
                        self.assertIsNotNone(getattr(bz_result, "title"))


if __name__ == "__main__":
    unittest.main()
