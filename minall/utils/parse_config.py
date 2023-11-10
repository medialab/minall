import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml


@dataclass
class APIKeys:
    buzzsumo_token: Optional[str]
    crowdtangle_token: Optional[str]
    crowdtangle_rate_limit: Optional[str]
    youtube_key: Optional[List[str]]

    def __init__(self, config: str | dict | None):
        if config:
            if isinstance(config, str):
                parsed_config = self.load_config_file(config)
            else:
                parsed_config = config
            self.buzzsumo_token = parsed_config["buzzsumo"]["token"]
            self.crowdtangle_token = parsed_config["crowdtangle"]["token"]
            self.crowdtangle_rate_limit = parsed_config["crowdtangle"]["rate_limit"]
            yt_keys = parsed_config["youtube"]["key"]
            if isinstance(yt_keys, list):
                self.youtube_key = yt_keys
            else:
                self.youtube_key = parsed_config["youtube"]["key"].split(",")
        else:
            self.buzzsumo_token = os.environ.get("BUZZSUMO_TOKEN")
            self.crowdtangle_token = os.environ.get("CROWDTANGLE_TOKEN")
            self.crowdtangle_rate_limit = os.environ.get("CROWDTANGLE_RATE_LIMIT")
            youtube_key = os.environ.get("YOUTUBE_KEY")
            if youtube_key:
                self.youtube_key = youtube_key.split(",")
            else:
                self.youtube_key = []

    @property
    def env_string(self) -> str:
        return "BUZZSUMO_TOKEN={bz}\nCROWDTANGLE_TOKEN={ct}\nCROWDTANGLE_RATE_LIMIT={crl}\nYOUTUBE_KEY={yt}\n".format(
            bz=self.buzzsumo_token,
            ct=self.crowdtangle_token,
            crl=self.crowdtangle_rate_limit,
            yt=self.youtube_key,
        )

    def load_config_file(self, config_file: str) -> dict:
        with open(config_file) as f:
            extension = Path(config_file).suffix
            if extension == ".json":
                return json.load(f)
            elif extension == ".yml" or extension == ".yaml":
                return yaml.safe_load(f)
            else:
                raise OSError
