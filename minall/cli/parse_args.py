from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path


def dir_path(string):
    if Path(string).is_dir():
        return string
    else:
        Path(string).mkdir(exist_ok=True)
        [p.mkdir(exist_ok=True) for p in Path(string).parents]
        return string


def file_path(string):
    if Path(string).is_file():
        return string
    else:
        raise FileNotFoundError(string)


def has_parent(string):
    [p.mkdir(exist_ok=True) for p in Path(string).parents]
    return string


CLI_ARGS = [
    "database",
    "config",
    "output_dir",
    "links_file",
    "url_col",
    "shared_content_file",
    "buzzsumo_only",
]


def cli_args() -> dict:
    parser = ArgumentParser(
        add_help=True, prog="Minall", formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--database",
        dest="database",
        required=False,
        type=has_parent,
        help="[Optional] Path to SQLite database. If not given, database written to memory.",
    )
    parser.add_argument(
        "--config",
        dest="config",
        type=file_path,
        required=False,
        help="[Optional] Path to configuration file. If not given, environment variables are expected.",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        type=dir_path,
        required=True,
        help="[Required] Path to directory in which a links and shared_content file will be written.",
    )
    parser.add_argument(
        "--links",
        dest="links_file",
        type=file_path,
        required=True,
        help="[Required] Path to links file.",
    )
    parser.add_argument(
        "--url-col",
        dest="url_col",
        type=str,
        required=True,
        help="[Required] Name of URL column in links file.",
    )
    parser.add_argument(
        "--shared-content",
        dest="shared_content_file",
        type=file_path,
        required=False,
        help="[Optional] Path to shared_content file.",
    )
    parser.add_argument(
        "--buzzsumo-only",
        dest="buzzsumo_only",
        default=False,
        required=False,
        action="store_true",
        help="[Optional] Flag indicating only Buzzsumo API will be called on links file.",
    )
    args = parser.parse_args()
    return args.__dict__
