import csv
from pathlib import Path
from typing import List

from minall.tables.links.constants import LinksConstants


def add_data(data: List[str], outfile: Path):
    with open(outfile, "w") as f:
        writer = csv.DictWriter(f, fieldnames=LinksConstants.col_names)
        writer.writeheader()
        [
            writer.writerow({"url": url, "work_type": "SocialMediaPosting"})
            for url in data
        ]
