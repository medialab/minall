import csv
import unittest
from pathlib import Path

from minet.twitter import TwitterGuestAPIScraper
from minet.loggers import sleepers_logger
from minet.cli.utils import CLIRetryerHandler

sleepers_logger.addHandler(CLIRetryerHandler())

from minall.enrichment.enrichment import Enrichment
from minall.enrichment.twitter.get_data import get_twitter_data
from minall.main import Minall
from minall.utils.parse_config import APIKeys
from tests.base import BaseTest


class Twitter(BaseTest):
    def setUp(self) -> None:
        # Set up out-files
        self.outdir = Path(__file__).parent.joinpath("twitter_test_results")
        self.outdir.mkdir(exist_ok=True)
        self.links_outfile = self.outdir.joinpath("links.csv")
        self.shared_content_outfile = self.outdir.joinpath("shared_content.csv")

        # Set up in-file
        self.links_infile = Path(__file__).parent.joinpath("tweets.csv")

        # Set up scraper and keys
        self.scraper = TwitterGuestAPIScraper()
        self.keys = APIKeys(self.config)

    def test_module(self):
        get_twitter_data(
            DATA,
            links_outfile=self.links_outfile,
            shared_content_outfile=self.shared_content_outfile,
        )
        with open(self.links_outfile) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.assertEqual(row["domain"], "twitter.com")
                self.assertEqual(row["work_type"], "SocialMediaPosting")
                self.assertEqual(row["creator_type"], "defacto:SocialMediaAccount")
                break

    def test_workflow(self):
        with open(self.links_outfile, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["url"])
            writer.writerow(
                ["https://twitter.com/Paris2024/status/1551605445156012038"]
            )

        app = Minall(
            database=None,
            config=None,
            output_dir=self.links_outfile.parent,
            links_file=self.links_outfile,
            url_col="url",
        )
        app.collect_and_coalesce()
        app.export()

        with open(app.links_table.outfile) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.assertEqual(row["domain"], "twitter.com")
                self.assertEqual(row["work_type"], "SocialMediaPosting")
                self.assertEqual(row["creator_type"], "defacto:SocialMediaAccount")
                break

    def tearDown(self) -> None:
        # Empty the out-file directory
        for file in self.outdir.iterdir():
            file.unlink()
        # Remove the out-file directory
        self.outdir.rmdir()
        # Remove the in-file
        if self.links_infile.is_file():
            self.links_infile.unlink()
        return super().tearDown()


DATA = [
    "https://twitter.com/silvano_trotta/status/1735765521595875777",
    "https://twitter.com/ResiIsrael/status/1740396336162193632",
    "https://twitter.com/RussieInfos/status/1741767581382410595",
    "https://twitter.com/Croquignol2A/status/1731921054631592062?s=20",
    "https://twitter.com/CH_Gallois/status/1731268150669255163",
    "https://twitter.com/ReaActuelle/status/1736431767509168298",
    "https://twitter.com/silvano_trotta/status/1733485827827581146",
    "https://twitter.com/GibertiePatrice/status/1733763332878868813",
    "https://twitter.com/PressTVFrench/status/1734793757399101480",
    "https://twitter.com/silvano_trotta/status/1731274174197326301",
    "https://twitter.com/Collectifvigi/status/1725121262177915217",
    "https://twitter.com/BlackBondPtv/status/1728860184683164147",
    "https://twitter.com/claudeelkhal/status/1725772883169845309",
    "https://twitter.com/EricArchambaul7/status/1708815296146895184",
    "https://twitter.com/patateMiDouce/status/1724737737029239202",
    "https://twitter.com/FilFrance/status/1723664236952392159",
    "https://twitter.com/JASMilovavitch/status/1721492403553759396",
    "https://twitter.com/Collectifvigi/status/1721248330255118363",
    "https://twitter.com/I_Desouche/status/1714593184179773523",
    "https://twitter.com/Conflitlive/status/1714513672326807912",
    "https://twitter.com/BPartisans/status/1713502496671306103",
    "https://twitter.com/Linfo24_7/status/1712125817965236437",
    "https://twitter.com/FarafinaW/status/1709331924370477219",
    "https://twitter.com/elonmusk/status/1706676593261785178",
    "https://twitter.com/Renaissance/status/1701243279591854100/photo/1",
    "https://twitter.com/cab2626/status/1695731492725432544",
    "https://twitter.com/silvano_trotta/status/1694304443817234724",
]


if __name__ == "__main__":
    unittest.main()
