import itertools
import os
import time
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
logfile = Path.cwd().joinpath("buzzsumo.log")


BEGINDATE = int(datetime.strptime("2020-01-01", "%Y-%m-%d").timestamp())

ENDDATE = int(
    datetime.strptime(
        datetime.utcnow().isoformat().split("T")[0], "%Y-%m-%d"
    ).timestamp()
)

# URL that Buzzsumo API has indexed
EXAMPLES_WITH_RESULTS = [
    "https://www.lemonde.fr/idees/article/2023/10/23/maintenir-la-pression-pour-lutter-contre-l-evasion-fiscale_6196088_3232.html",
    "https://www.youtube.com/watch?v=bj6PcWBgVN4",
    "https://planetes360.fr/attention-multiplication-par-5-des-deces-cardiaques-soudains-chez-les-joueurs-de-la-fifa-en-2021/",
    "https://www.francesoir.fr/politique-monde/robert-malone-plaidoyer-vaccination-enfants",
    "https://planetes360.fr/pr-perronne-il-y-a-une-epidemie-de-sterilite-chez-les-femmes-de-30-ans-vaccinees-contre-le-covid/",
    "https://www.20minutes.fr/sante/3291615-20220517-bordeaux-systeme-regulation-patients-entre-vigueur-soir-urgences-chu-pellegrin",
    "https://www.francetvinfo.fr/economie/energie/inflation-plusieurs-piscines-contraintes-de-fermer-en-france-en-raison-de-lexplosion-des-prix-de-lenergie_5343667.html",
    "https://cogiito.com/a-la-une/ils-ont-ose-la-croix-rouge-americaine-surprise-en-train-de-melanger-du-sang-de-vaccine-avec-du-sang-de-non-vaccine/",
    "https://atlantico.fr/article/pepite/la-mairie-de-paris-refuse-toujours-de-transmettre-les-notes-de-frais-d-anne-hidalgo-malgre-les-requetes-du-journaliste-stefan-de-vries-conseil-d-etat-avocat-association-journalisme-frais-soutien-aide",
    "https://www.tf1info.fr/replay-lci/video-l-interview-politique-aurore-berge-presidente-du-groupe-renaissance-a-l-assemblee-nationale-invitee-d-adrien-gindre-dans-les-matins-lci-2241193.html",
    "https://cogiito.com/a-la-une/le-forum-economique-mondial-dit-que-le-seul-moyen-de-sauver-lhumanite-est-de-liberer-les-pedophiles/",
    "https://www.01net.com/actualites/chatgpt-assez-intelligent-passer-examen-droit.html",
    "https://1scandal.com/le-cdc-avertit-que-plusieurs-piqures-covid-diminuent-la-duree-de-vie-de-24-ans/",
    "https://perma.cc/GBY4-ZUWD",
    "https://archive.ph/IvOen",
    "https://web.archive.org/web/20230906094418/https://twitter.com/MK_Falcone/status/1698620530759176229",
    "https://www.francebleu.fr/infos/societe/suicide-d-un-ado-a-poissy-elisabeth-borne-reconnait-une-lettre-choquante-du-rectorat-adressee-aux-parents-6787291",
    "https://www.20minutes.fr/societe/4054036-20230921-meurthe-moselle-maire-prend-arrete-limiter-chaque-foyer-coq-deux-chiens",
    "https://web.archive.org/web/20231004073806/https://twitter.com/VictorSinclair3/status/1708794083961864539",
]

EXAMPLES_WITHOUT_RESULTS = [
    "https://twitter.com/patateMiDouce/status/1724737737029239202"
]

DATA = EXAMPLES_WITH_RESULTS + EXAMPLES_WITHOUT_RESULTS

N_DUPLICATES = 5


def duplicate_examples() -> List[str]:
    return list(
        itertools.chain.from_iterable(
            [list(itertools.repeat(d, N_DUPLICATES)) for d in DATA]
        )
    )


class ThreadedClient:
    def __init__(self, token: str) -> None:
        self.client = BuzzSumoAPIClient(token=token)

    def __call__(self, url: str) -> Tuple[str, BuzzsumoArticle | None]:
        result = self.client.exact_url(url, BEGINDATE, ENDDATE)
        return url, result


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.token = os.environ["BUZZSUMO_TOKEN"]
        self.client = BuzzSumoAPIClient(token=self.token)
        self.data = DATA
        self.progress_bar = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )
        self.threaded_client = ThreadedClient(token=self.token)
        print("Wait 6 minutes to reset rate limit and clear cache.")
        time.sleep(60 * 6)

    def test_amultithread(self) -> None:
        # Affirm the token isn't None
        token = self.token
        assert token

        with open(logfile, "a") as f:
            with Timer(
                file=f,
                name=f"[{datetime.utcnow()}] Multi-thread on {len(self.data)} URLs",
            ), self.progress_bar as p, ThreadPoolExecutor() as executor:
                t = p.add_task("Multithread", total=len(self.data))

                for result in executor.map(self.threaded_client, self.data):
                    url, bz_result = result
                    # Advance the progress bar and assert known matches aren't None
                    p.advance(t)
                    if url in EXAMPLES_WITH_RESULTS:
                        self.assertIsNotNone(getattr(bz_result, "title"))

    def test_bloop(self) -> None:
        # Affirm the token isn't None
        token = self.token
        assert token

        with open(logfile, "a") as f:
            with Timer(
                file=f,
                name=f"[{datetime.utcnow()}] Single-thread on {len(self.data)} URLs",
            ), self.progress_bar as p:
                task = p.add_task("Single-thread", total=len(self.data))

                for url in self.data:
                    # Call minet's Buzzsumo API client
                    result = self.client.exact_url(
                        search_url=url,
                        begin_timestamp=BEGINDATE,
                        end_timestamp=ENDDATE,
                    )

                    # Advance the progress bar and assert known matches aren't None
                    p.advance(task)
                    if url in EXAMPLES_WITH_RESULTS:
                        self.assertIsNotNone(getattr(result, "title"))


if __name__ == "__main__":
    unittest.main()
