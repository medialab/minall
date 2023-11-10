import csv
from pathlib import Path

from minall.tables.links.constants import LinksConstants


def add_data(data: list[tuple[str, str]], outfile: Path):
    with open(outfile, "w") as f:
        writer = csv.DictWriter(f, fieldnames=LinksConstants.col_names)
        writer.writeheader()
        [
            writer.writerow({"url": url, "work_type": "SocialMediaPosting"})
            for url in data
        ]
