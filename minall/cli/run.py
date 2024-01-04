# minall/cli/run.py

"""CLI action for minall workflow.

This module contains the function `cli()`, which runs the minall workflow as a CLI tool.

The function `cli()` requests and parses the command-line arguments that are necessary to create an instance of the `Minall` class. Then, it deploys the `Minall` class's workflow.
"""

from minall.cli.parse_args import cli_args
from minall.main import Minall


def cli():
    """Run minall workflow from the command line."""

    args = cli_args()

    app = Minall(**args)

    app.collect_and_coalesce()

    app.export()


if __name__ == "__main__":
    cli()
