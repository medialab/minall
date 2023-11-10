import csv
import unittest
from pathlib import Path

from minall.main import Minall


class TestLinksTable(unittest.TestCase):
    OUTDIR = Path.cwd().joinpath("tests")
    LINKS_FILE = OUTDIR.joinpath("links.csv")

    def setUp(self) -> None:
        with open(self.LINKS_FILE, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["my_url", "seq", "first_name", "last_name"])
            writer.writerow(
                [
                    "https://www.github.com/medialab/minall",
                    "first instance of URL",
                    "Sophie",
                    "Gail",
                ]
            )
            writer.writerow(
                [
                    "https://www.github.com/medialab/minall",
                    "second instance of URL, should be ignored",
                    "Pauline",
                    "Viardot",
                ]
            )

    def test(self):
        app = Minall(
            database=":memory:",
            config={},
            output_dir=str(self.OUTDIR),
            links_file=str(self.LINKS_FILE),
            url_col="my_url",
            shared_content_file=None,
            buzzsumo_only=True,
        )
        links_table = app.links_table
        cursor = links_table.connection.cursor()
        relation = cursor.execute(
            f"SELECT * from {links_table.table.table_name}"
        ).fetchall()

        # 2 Duplicated URLs in in-file should return SQL table of 1 row
        assert len(relation) == 1

        # First instance of URL should be only row in SQL relation
        row_dict = dict(zip(links_table.columnparser.infile_standardized, relation[0]))
        assert row_dict["seq"] == "first instance of URL"

        self.LINKS_FILE.unlink()


if __name__ == "__main__":
    unittest.main()
