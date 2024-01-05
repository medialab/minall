# minall/cli/parse_args.py

"""Helper functions for CLI action.

This module contains the following helper functions for parsing command-line arguments:

- `cli_args()` - Parse CLI arguments.
- `dir_path(path_name)` - Create directory and necessary parent directories.
- `file_path(path_name)` - Verify existence of given file.
- `has_parent(path_name)` - Create necessary parent directories for file path.
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path


def dir_path(path_name: str) -> str:
    """Function to convert CLI argument to created directory.

    Args:
        path_name (str): Path to target directory.

    Returns:
        str: Path to prepared directory.
    """
    if Path(path_name).is_dir():
        return path_name
    else:
        Path(path_name).mkdir(exist_ok=True)
        [p.mkdir(exist_ok=True) for p in Path(path_name).parents]
        return path_name


def file_path(path_name: str) -> str:
    """Function to convert CLI argument to verified, found file path.

    Args:
        path_name (str): Path to data file.

    Raises:
        FileNotFoundError: Data file not found at given path.

    Returns:
        str: Verified path to data file.
    """
    if Path(path_name).is_file():
        return path_name
    else:
        raise FileNotFoundError(path_name)


def has_parent(path_name: str) -> str:
    """Function to convert CLI argument to file path with created parent directories.

    Args:
        path_name (str): Path to out-file.

    Returns:
        str: Path to out-file with created parent directories.
    """
    [p.mkdir(exist_ok=True) for p in Path(path_name).parents]
    return path_name


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
    """Function to call and parse command-line arguments.

    Returns:
        dict: Dictionary of parsed command-line arguments.
    """
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
