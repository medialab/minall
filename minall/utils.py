import json
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import dotenv_values
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)


def parse_cli_args(
    links_file: str,
    shared_content_file: str | None,
    output_dir: str,
    buzzsumo_only: bool,
    config_file: str,
) -> None:
    # Parse CLI argument for path to URLs file
    if not Path(links_file).is_file():
        raise FileNotFoundError
    INPUT_LINKS = "INPUT_LINKS={}".format(links_file)

    # Parse CLI argument for path to shared media content file
    if shared_content_file and Path(shared_content_file).is_file():
        SHARED_CONTENT = "INPUT_SHARED_CONTENT={}".format(shared_content_file)
    else:
        SHARED_CONTENT = ""

    # Parse CLI argument for path to output directory
    Path(output_dir).mkdir(exist_ok=True)
    OUTPUT_DIR = "OUTPUT_DIR={}".format(output_dir)

    # Boolean for whether or not to only collect Buzzsumo data
    BUZZSUMO_ONLY = "BUZZSUMO_ONLY={}".format(buzzsumo_only)

    # Parse configuration file
    with open(config_file) as f:
        config = json.load(f)
    if not isinstance(config, dict):
        raise ValueError
    CROWDTANGLE_TOKEN = "CROWDTANGLE_TOKEN={}".format(config["crowdtangle"]["token"])
    CROWDTANGLE_RATE_LIMIT = "CROWDTANGLE_RATE_LIMIT={}".format(
        config["crowdtangle"]["rate_limit"]
    )
    YOUTUBE_KEY_LIST = "YOUTUBE_KEYS={}".format(config["youtube"]["key"])
    BUZZSUMO_TOKEN = "BUZZSUMO_TOKEN={}".format(config["buzzsumo"]["token"])

    # Clear .env file of any past variables
    dotenv_path = Path.cwd().joinpath(".env")
    if dotenv_path.is_file():
        dotenv_path.unlink()
    dotenv_path.touch()

    env = "{bz_only}\n{input}\n{output}\n{ct_token}\n{ct_rl}\n{yt_key}\n{bz_token}\n{shared_content}".format(
        bz_only=BUZZSUMO_ONLY,
        input=INPUT_LINKS,
        output=OUTPUT_DIR,
        ct_token=CROWDTANGLE_TOKEN,
        ct_rl=CROWDTANGLE_RATE_LIMIT,
        yt_key=YOUTUBE_KEY_LIST,
        bz_token=BUZZSUMO_TOKEN,
        shared_content=SHARED_CONTENT,
    )

    # Register CLI arguments as Python environment variables
    dotenv_path.write_text(env)


@contextmanager
def progress_bar():
    with Progress(
        TextColumn("\t{task.description}"),
        MofNCompleteColumn(),
        BarColumn(),
        TimeElapsedColumn(),
        expand=True,
    ) as progress:
        yield progress


@dataclass
class EnvVars:
    bz_only: bool = False
    bz_token: str | None = None
    ct_token: str | None = None
    ct_rate_limit: int | None = None
    yt_keys: list = field(default_factory=list)
    outdir: Path | None = None


def parse_env_vars() -> EnvVars:
    config = dotenv_values(Path.cwd().joinpath(".env"))
    BUZZSUMO_TOKEN = config.get("BUZZSUMO_TOKEN")
    BUZZSUMO_ONLY = config.get("BUZZSUMO_ONLY")
    CROWDTANGLE_TOKEN = config.get("CROWDTANGLE_TOKEN")
    CROWDTANGLE_RATE_LIMIT = config.get("CROWDTANGLE_RATE_LIMIT")
    YOUTUBE_KEY_LIST = config.get("YOUTUBE_KEYS")
    OUTPUT_DIR = config.get("OUTPUT_DIR")

    env_vars = EnvVars()

    if BUZZSUMO_ONLY == "True":
        env_vars.bz_only = True
    else:
        env_vars.bz_only = False

    if YOUTUBE_KEY_LIST:
        env_vars.yt_keys = YOUTUBE_KEY_LIST.split(",")

    if CROWDTANGLE_RATE_LIMIT:
        try:
            env_vars.ct_rate_limit = int(CROWDTANGLE_RATE_LIMIT)
        except Exception as _:
            raise TypeError

    if OUTPUT_DIR:
        env_vars.outdir = Path(OUTPUT_DIR)

    env_vars.bz_token = BUZZSUMO_TOKEN
    env_vars.ct_token = CROWDTANGLE_TOKEN

    return env_vars
