# minall/cli/run.py

"""CLI action for minall workflow.

This module contains the function `cli()`, which runs the minall workflow as a CLI tool. Using the imported helper function `cli_args()`, the function parses command-line arguments and uses the necessary parameters to create and instance of the `Minall` class. Finally, the function deploys the whole `Minall` workflow. 
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
