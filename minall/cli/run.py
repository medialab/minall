# minall/cli/run.py

"""CLI action for minall workflow.

This module runs the minall workflow as a CLI tool.

The module contains the following function:

- `cli()` - 
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
