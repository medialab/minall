import csv
from pathlib import Path

from minall.links.constants import LINKS_FIELDNAMES


def add_data(data: list[tuple[str, str]], outfile: Path):
    with open(outfile, "w") as f:
        writer = csv.DictWriter(f, fieldnames=LINKS_FIELDNAMES)
        writer.writeheader()
        [
            writer.writerow(
                {"url": url, "link_id": link_id, "type": "SocialMediaPosting"}
            )
            for url, link_id in data
        ]
