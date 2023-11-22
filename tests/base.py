import os
import unittest
from pathlib import Path

import yaml

# Config YAML at root of project directory
CONFIG_PATH = Path(__file__).parent.parent.joinpath("config.yml")
LOG_FILE = Path(__file__).parent.joinpath("minall.log")


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if CONFIG_PATH.is_file():
            with open(CONFIG_PATH) as f:
                config = yaml.safe_load(f)
                os.environ["BUZZSUMO_TOKEN"] = config["buzzsumo"]["token"]
                os.environ["CROWDTANGLE_RATE_LIMIT"] = str(
                    config["crowdtangle"]["rate_limit"]
                )
                os.environ["CROWDTANGLE_TOKEN"] = config["crowdtangle"]["token"]
                os.environ["YOUTUBE_KEY"] = config["youtube"]["key"]
                cls.config = config
        else:
            cls.config = {
                "buzzsumo": {"token": os.environ["BUZZSUMO_TOKEN"]},
                "crowdtangle": {
                    "token": os.environ["CROWDTANGLE_TOKEN"],
                    "rate_limit": 10,
                },
                "youtube": {"key": os.environ["YOUTUBE_KEY"]},
            }

    @classmethod
    def tearDownClass(cls) -> None:
        if LOG_FILE.is_file():
            LOG_FILE.unlink()
