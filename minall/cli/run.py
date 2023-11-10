from minall.cli.parse_args import cli_args
from minall.main import Minall


def cli():
    args = cli_args()

    app = Minall(**args)

    app.collect_and_coalesce()

    app.export()


if __name__ == "__main__":
    cli()
