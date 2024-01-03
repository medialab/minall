# minall/utils/parse_config.py

"""Data class to store and manage minet client credentials.

The class `APIKeys` contains the following methods and properties:

- `__init__(config)` - Parses the minet client configuration details.
- `env_string()` - Formats the minet client credentials as an environment variable string.
- `load_config_file(config_file)` - Parse client configuration details from JSON or YAML file.
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml


@dataclass
class APIKeys:
    """Data class to store and manage minet client credentials.

    Attributes:
        buzzsumo_token (Optional[str]): Buzzsumo API token. Optional.
        crowdtangle_token (Optional[str]):  CrowdTangle API token. Optional.
        crowdtangle_rate_limit (Optional[str]): CrowdTangle API rate limit, cast as a string. Optional.
        youtube_key (Optional[List[str]]) : List of YouTube API keys. Optional.
    """

    buzzsumo_token: Optional[str]
    crowdtangle_token: Optional[str]
    crowdtangle_rate_limit: Optional[str]
    youtube_key: Optional[List[str]]

    def __init__(self, config: str | dict | None = None):
        """Parse and save minet API client configuration details.

        Examples:
            >>> keys = APIKeys(config={"youtube": {"key": "key1,key2"}})
            >>> keys
            APIKeys(buzzsumo_token=None, crowdtangle_token=None, crowdtangle_rate_limit=None, youtube_key=["key1", "key2"])
            >>> keys.youtube_key
            ["key1, "key2]

        Args:
            config (str | dict | None, optional): If string, string is treated like file path to JSON or YAML file that contains details; if dict, details are directly parsed; if None, details are searched from environment variables. Defaults to None.
        """
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
        r"""Formatted string for setting environment variables.

        Examples:
            >>> keys = APIKeys(config={'buzzsumo': {'token': 'bz_token'}, 'crowdtangle': {'token': 'ct_token', 'rate_limit': 10}, 'youtube': {'key': 'key1,key2'}})
            >>> keys.env_string
            "BUZZSUMO_TOKEN=bz_token\nCROWDTANGLE_TOKEN=ct_token\nCROWDTANGLE_RATE_LIMIT=10\nYOUTUBE_KEY=['key1', 'key2']\n"

        Returns:
            str: String declaring environment variables.
        """

        return "BUZZSUMO_TOKEN={bz}\nCROWDTANGLE_TOKEN={ct}\nCROWDTANGLE_RATE_LIMIT={crl}\nYOUTUBE_KEY={yt}\n".format(
            bz=self.buzzsumo_token,
            ct=self.crowdtangle_token,
            crl=self.crowdtangle_rate_limit,
            yt=self.youtube_key,
        )

    def load_config_file(self, config_file: str) -> dict:
        """Parse dictionary from JSON or YAML configuration file.

        Args:
            config_file (str): Path to JSON or YAML file.

        Raises:
            OSError: Error raised if given file path does not have the extension ".json", ".yml", or ".yaml".

        Returns:
            dict: Parsed dictionary from JSON or YAML configuration file.
        """

        with open(config_file) as f:
            extension = Path(config_file).suffix
            if extension == ".json":
                return json.load(f)
            elif extension == ".yml" or extension == ".yaml":
                return yaml.safe_load(f)
            else:
                raise OSError
